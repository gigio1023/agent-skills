#!/usr/bin/env python3
"""Bounded Cursor CLI invocation and private evidence, using Python stdlib only."""

import argparse
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import tempfile
import time

DEFAULT_MODEL = "cursor-grok-4.6-xhigh-fast"


def build_argv(executable, workspace, prompt, model=DEFAULT_MODEL, resume=None,
               mode="agent", yolo=True):
    argv = [executable, "--print", "--output-format", "stream-json",
            "--model", model, "--workspace", str(workspace)]
    if yolo:
        argv.append("--yolo")
    if mode != "agent":
        argv.extend(["--mode", mode])
    if resume is not None:
        argv.extend(["--resume", resume])
    return argv + ["--", prompt]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--prompt-file", type=Path, required=True,
                        help="UTF-8 packet; must contain no secrets (CLI uses argv)")
    parser.add_argument("--state-dir", type=Path,
                        default=Path.home() / ".local/state/cursor-cli-delegation")
    parser.add_argument("--agent", default="agent", help="executable path, not a shell command")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--resume", help="exact session ID, never latest")
    parser.add_argument("--mode", choices=["agent", "ask", "plan"], default="agent")
    parser.add_argument("--no-yolo", action="store_true", help="omit broad unattended approval")
    parser.add_argument("--timeout", type=float, help="optional wall-clock seconds before scoped cancellation; no deadline by default")
    args = parser.parse_args()
    if os.name != "posix":
        parser.error("requires POSIX process groups; use a host-native scoped runner elsewhere")
    if args.timeout is not None and (not math.isfinite(args.timeout) or args.timeout <= 0):
        parser.error("--timeout must be finite and positive")
    for label, value in [("model", args.model), ("resume", args.resume)]:
        if value is not None and (not value or value.startswith("-") or any(c.isspace() or ord(c) < 32 for c in value)):
            parser.error(f"--{label} must be an exact nonempty ID, not an option")
    package = Path(__file__).resolve().parent.parent
    args.state_dir = args.state_dir.expanduser().resolve()
    if args.state_dir == package or package in args.state_dir.parents:
        parser.error("runtime state must be outside the skill package")
    try:
        workspace = args.workspace.resolve(strict=True)
        if not workspace.is_dir():
            raise ValueError("workspace must be a directory")
        prompt_path = args.prompt_file.expanduser().resolve()
        if prompt_path == package or package in prompt_path.parents:
            raise ValueError("packet must be outside the skill package")
        prompt = prompt_path.read_text(encoding="utf-8")
        if not prompt.strip() or "\0" in prompt:
            raise ValueError("packet must be nonempty UTF-8 text without NUL")
    except (OSError, ValueError) as error:
        parser.error(str(error))
    os.umask(0o077)
    args.state_dir.mkdir(parents=True, exist_ok=True)
    run_dir = Path(tempfile.mkdtemp(prefix="run-", dir=args.state_dir))
    argv = build_argv(args.agent, workspace, prompt, args.model, args.resume,
                      args.mode, not args.no_yolo)
    started = time.time()
    issues = []
    process = None
    exit_code = None
    stop_reason = None
    interrupted = None

    def on_signal(signum, frame):
        nonlocal interrupted
        interrupted = signum

    previous = {sig: signal.signal(sig, on_signal) for sig in (signal.SIGINT, signal.SIGTERM)}
    with (run_dir / "stdout.log").open("wb") as stdout, (run_dir / "stderr.log").open("wb") as stderr:
        try:
            process = subprocess.Popen(argv, cwd=workspace, stdout=stdout, stderr=stderr,
                                       start_new_session=True)
            deadline = time.monotonic() + args.timeout if args.timeout is not None else math.inf
            while process.poll() is None and interrupted is None and time.monotonic() < deadline:
                time.sleep(0.05)
            if interrupted is not None or process.poll() is None:
                stop_reason = f"signal:{interrupted}" if interrupted else "timeout"
                if process.returncode is not None:
                    issues.append(f"{stop_reason}; leader already reaped; group cleanup skipped to avoid reused ID")
                else:
                    issues.append(f"{stop_reason}; owned process group cancellation attempted")
                    # No poll/wait between signals: keep the unreaped leader's ID reserved.
                    for sig in (signal.SIGTERM, signal.SIGKILL):
                        try:
                            os.killpg(process.pid, sig)
                        except ProcessLookupError:
                            pass
                        if sig == signal.SIGTERM:
                            time.sleep(0.2)
            exit_code = process.wait()
        except OSError as error:
            issues.append(f"launch failed: {error}")
    for sig, handler in previous.items():
        signal.signal(sig, handler)
    if exit_code != 0:
        issues.append("nonzero process exit")
    init = None
    result = None
    session_id = None
    malformed = invalid_session = conflicting_session = False
    # Stream the saved log one event at a time; never retain the transcript.
    with (run_dir / "stdout.log").open("rb") as stream, \
            (run_dir / "events.jsonl").open("w", encoding="utf-8") as output:
        for line in stream:
            if not line.strip():
                continue
            try:
                event = json.loads(line.decode("utf-8"))
                if not isinstance(event, dict):
                    raise ValueError("not an object")
            except ValueError:
                malformed = True
                continue
            output.write(json.dumps(event) + "\n")
            if init is None and event.get("subtype") == "init":
                init = event
            if event.get("type") == "result":
                result = event
            if "session_id" in event:
                supplied = event["session_id"]
                if not isinstance(supplied, str) or not supplied:
                    invalid_session = True
                elif session_id is None:
                    session_id = supplied
                elif supplied != session_id:
                    conflicting_session = True
    init = init or {}
    if malformed:
        issues.append("malformed stream event")
    if init.get("type") != "system" or not init.get("model"):
        issues.append("missing initialization/model evidence")
    if result is None or result.get("subtype") != "success" or result.get("is_error") is not False:
        issues.append("missing or unsuccessful terminal result")
    if invalid_session:
        issues.append("invalid supplied session identity")
    session_id = (result or {}).get("session_id") or init.get("session_id")
    if not isinstance(session_id, str) or not session_id:
        session_id = None
    if session_id is None or conflicting_session or (args.resume and session_id != args.resume):
        issues.append("missing or conflicting session identity")
    receipt = dict(workspace=str(workspace), requested_model=args.model,
                   argv=argv[:-1] + ["<prompt omitted>"], reported_model=init.get("model"),
                   resumed_session_id=args.resume, session_id=session_id,
                   process_exit_code=exit_code, pid=process.pid if process else None,
                   stop_reason=stop_reason, result=result, timeout_seconds=args.timeout,
                   transport_status="incomplete" if issues else "complete",
                   issues=issues, task_status="unverified",
                   started_at=started, duration_seconds=time.time() - started,
                   run_dir=str(run_dir.resolve()))
    receipt_path = run_dir / "receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"receipt": str(receipt_path.resolve())}))
    if interrupted is not None:
        return 128 + interrupted
    if stop_reason == "timeout":
        return 124
    if process is None:
        return 127
    return (128 - exit_code if exit_code < 0 else exit_code) if exit_code else (1 if issues else 0)


if __name__ == "__main__":
    raise SystemExit(main())
