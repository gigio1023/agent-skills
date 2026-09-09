"""Native runner regression tests; all subprocess fixtures are synthetic, not Cursor evidence."""
import importlib.util
from pathlib import Path
import unittest
import json
import os
import subprocess
import sys
import tempfile

SCRIPT = Path(__file__).with_name("cursor_run.py")


class RunnerTests(unittest.TestCase):
    def invoke(self, source, *extra):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        fake = root / "synthetic-agent"
        fake.write_text(f"#!{sys.executable}\n" + source)
        fake.chmod(0o700)
        prompt = root / "prompt.txt"
        prompt.write_text('--looks-like-flag; $(touch unwanted)')
        state = root / "state"
        command = [sys.executable, "-B", str(SCRIPT), "--agent", str(fake),
                   "--workspace", str(root), "--prompt-file", str(prompt),
                   "--state-dir", str(state), *extra]
        result = subprocess.run(command, capture_output=True, text=True, timeout=15)
        receipts = list(state.glob("*/receipt.json"))
        self.assertEqual(len(receipts), 1, result.stdout + result.stderr)
        return result, json.loads(receipts[0].read_text()), receipts[0].parent

    def test_cancellation_never_signals_reaped_leader(self):
        from unittest.mock import patch, Mock
        import signal
        spec = importlib.util.spec_from_file_location("cursor_run", SCRIPT)
        assert spec is not None and spec.loader is not None
        runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(runner)
        with tempfile.TemporaryDirectory() as root:
            prompt = Path(root) / "prompt"
            prompt.write_text("test")
            handlers = {}
            process = Mock(pid=12345, returncode=None)

            def poll():
                handlers[signal.SIGTERM](signal.SIGTERM, None)
                process.returncode = 0
                return 0

            def register(sig, handler):
                handlers[sig] = handler
                return signal.SIG_DFL

            process.poll.side_effect = poll
            process.wait.return_value = 0
            argv = [str(SCRIPT), "--workspace", root, "--prompt-file", str(prompt),
                    "--state-dir", str(Path(root) / "state")]
            with patch.object(sys, "argv", argv), patch.object(runner.signal, "signal", register), \
                    patch.object(runner.subprocess, "Popen", return_value=process), \
                    patch.object(runner.os, "killpg") as killpg, patch("builtins.print"):
                self.assertEqual(runner.main(), 143)
            killpg.assert_not_called()
            receipt = json.loads(next((Path(root) / "state").glob("*/receipt.json")).read_text())
            self.assertTrue(any("reaped" in issue and "cleanup" in issue for issue in receipt["issues"]))

    def test_every_supplied_session_id_is_valid_and_consistent(self):
        for invalid in [123, "", None, False, [], {}, "other-session"]:
            for position in [0, 1, 2]:
                with self.subTest(invalid=invalid, position=position):
                    events = [
                        dict(type="system", subtype="init", model="Synthetic", session_id="test-session"),
                        dict(type="assistant", session_id="test-session"),
                        dict(type="result", subtype="success", is_error=False, session_id="test-session"),
                    ]
                    events[position]["session_id"] = invalid
                    source = "print(" + repr("\n".join(json.dumps(e) for e in events)) + ")"
                    result, receipt, _ = self.invoke(source)
                    self.assertEqual(result.returncode, 1)
                    self.assertEqual(receipt["transport_status"], "incomplete")
                    self.assertTrue(any("session" in issue for issue in receipt["issues"]))

    def test_stream_parsing_does_not_retain_transcript_or_duplicate_issues(self):
        from unittest.mock import patch
        import tracemalloc
        spec = importlib.util.spec_from_file_location("cursor_run", SCRIPT)
        assert spec is not None and spec.loader is not None
        runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(runner)
        with tempfile.TemporaryDirectory() as root:
            prompt = Path(root) / "prompt"
            prompt.write_text("test")
            fake = Path(root) / "synthetic-agent"
            fake.write_text(f"#!{sys.executable}\n" + '''import json
print(json.dumps(dict(type="system", subtype="init", model="Synthetic", session_id="test-session")))
for i in range(6000):
    print(json.dumps(dict(type="assistant", text="x" * 2048, session_id="test-session")))
for i in range(1000):
    print("invalid JSON")
print(json.dumps(dict(type="result", subtype="success", is_error=False, session_id="test-session")))
''')
            fake.chmod(0o700)
            argv = [str(SCRIPT), "--workspace", root, "--prompt-file", str(prompt),
                    "--state-dir", str(Path(root) / "state"), "--agent", str(fake)]
            tracemalloc.start()
            try:
                with patch.object(sys, "argv", argv), patch("builtins.print"):
                    self.assertEqual(runner.main(), 1)
                _, peak = tracemalloc.get_traced_memory()
            finally:
                tracemalloc.stop()
            self.assertLess(peak, 2 * 1024 * 1024, "full transcript retained in memory")
            receipt_path = next((Path(root) / "state").glob("*/receipt.json"))
            receipt = json.loads(receipt_path.read_text())
            self.assertEqual(receipt["issues"].count("malformed stream event"), 1)
            with (receipt_path.parent / "events.jsonl").open() as stream:
                self.assertEqual(sum(1 for _ in stream), 6002)

    def test_prompt_inside_package_or_symlink_is_rejected_before_read(self):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)
            alias = root / "packet-link"
            alias.symlink_to(SCRIPT.parent.parent / "SKILL.md")
            for prompt in [SCRIPT.parent.parent / "SKILL.md", alias,
                           SCRIPT.parent / "missing-packet"]:
                with self.subTest(prompt=prompt):
                    result = subprocess.run(
                        [sys.executable, "-B", str(SCRIPT), "--workspace", str(root),
                         "--prompt-file", str(prompt), "--state-dir", str(root / "state"),
                         "--agent", "/nonexistent/cursor-test-agent"],
                        capture_output=True, text=True, timeout=10)
                    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                    self.assertIn("packet must be outside the skill package", result.stderr)
                    self.assertFalse((root / "state").exists())

    def test_reference_keeps_deadline_optional_in_ordinary_examples(self):
        reference = (SCRIPT.parent.parent / "references/cursor-agent-cli.md").read_text()
        self.assertNotIn("--timeout 600", reference)
        self.assertIn("omitted means no runner-imposed deadline", reference)

    def test_session_only_in_intermediate_event_is_incomplete(self):
        events = [dict(type="system", subtype="init", model="Synthetic"),
                  dict(type="assistant", session_id="test-session"),
                  dict(type="result", subtype="success", is_error=False)]
        source = "print(" + repr("\n".join(json.dumps(e) for e in events)) + ")"
        result, receipt, _ = self.invoke(source)
        self.assertEqual(result.returncode, 1)
        self.assertTrue(any("session" in issue for issue in receipt["issues"]))
        self.assertIsNone(receipt["session_id"])

    def test_private_receipt_and_exact_resume(self):
        source = '''import json, sys
print(json.dumps({"type": "system", "subtype": "init", "session_id": "test-session", "model": "Synthetic label"}))
print(json.dumps({"type": "result", "subtype": "success", "is_error": False, "session_id": "test-session", "result": "fixture response"}))
print("fixture stderr", file=sys.stderr)
assert sys.argv[sys.argv.index("--resume") + 1] == "test-session"
assert sys.argv[-1] == '--looks-like-flag; $(touch unwanted)'
'''
        result, receipt, run_dir = self.invoke(source, "--resume", "test-session")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(receipt["process_exit_code"], 0)
        self.assertEqual(receipt["session_id"], "test-session")
        self.assertEqual(receipt["resumed_session_id"], "test-session")
        self.assertEqual(receipt["reported_model"], "Synthetic label")
        self.assertEqual(receipt["task_status"], "unverified")
        self.assertEqual(receipt["transport_status"], "complete")
        self.assertEqual(receipt["result"]["result"], "fixture response")
        self.assertEqual(len((run_dir / "events.jsonl").read_text().splitlines()), 2)
        self.assertEqual((run_dir / "stderr.log").read_text(), "fixture stderr\n")
        self.assertNotIn("$(touch", json.dumps(receipt))
        self.assertFalse((run_dir.parent.parent / "unwanted").exists())
        self.assertEqual(run_dir.stat().st_mode & 0o777, 0o700)
        for path in run_dir.iterdir():
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)

    def test_timeout_is_opt_in_and_recorded(self):
        source = '''import json
print(json.dumps({"type": "system", "subtype": "init", "session_id": "test-session", "model": "Synthetic label"}))
print(json.dumps({"type": "result", "subtype": "success", "is_error": False, "session_id": "test-session"}))
'''
        _, receipt, _ = self.invoke(source)
        self.assertIsNone(receipt["timeout_seconds"])
        _, receipt, _ = self.invoke(source, "--timeout", "5")
        self.assertEqual(receipt["timeout_seconds"], 5)

    def test_incomplete_evidence_and_nonzero_exit(self):
        cases = [
            ('print("not JSON")', 1, "malformed"),
            ('print("[]")', 1, "malformed"),
            ('print("{}")', 1, "terminal"),
            ('import sys; sys.exit(7)', 7, "exit"),
            ('print(\'{"type":"result","subtype":"error","is_error":true}\')', 1, "terminal"),
            ('print(\'{"type":"result","subtype":"success","session_id":"other"}\')', 1, "session"),
        ]
        for source, code, reason in cases:
            with self.subTest(reason=reason, source=source):
                result, receipt, _ = self.invoke(source, "--resume", "test-session")
                self.assertEqual(result.returncode, code)
                self.assertEqual(receipt["transport_status"], "incomplete")
                self.assertTrue(any(reason in issue for issue in receipt["issues"]), receipt)
                self.assertEqual(receipt["task_status"], "unverified")

    @unittest.skipUnless(os.name == "posix", "POSIX scoped cancellation")
    def test_timeout_stops_owned_group_not_unrelated_process(self):
        unrelated = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(20)"])
        self.addCleanup(unrelated.wait)
        self.addCleanup(unrelated.terminate)
        source = '''import os, signal, subprocess, sys, time
from pathlib import Path
child = subprocess.Popen([sys.executable, "-c", "import signal,time; signal.signal(signal.SIGTERM, signal.SIG_IGN); time.sleep(1.5); open('escaped', 'w').write('bad'); time.sleep(20)"])
print('{"type":"system","subtype":"init","session_id":"test-session"}', flush=True)
time.sleep(20)
'''
        result, receipt, run_dir = self.invoke(source, "--timeout", "0.4")
        self.assertEqual(result.returncode, 124)
        self.assertEqual(receipt["stop_reason"], "timeout")
        self.assertIsNotNone(receipt["pid"])
        self.assertEqual(receipt["transport_status"], "incomplete")
        self.assertIsNone(unrelated.poll())
        import time
        time.sleep(1.6)
        self.assertFalse((run_dir.parent.parent / "escaped").exists())

    def test_spawn_failure_retains_receipt(self):
        result, receipt, _ = self.invoke("", "--agent", "/nonexistent/cursor-test-agent")
        self.assertEqual(result.returncode, 127)
        self.assertIsNone(receipt["process_exit_code"])
        self.assertTrue(any("launch" in issue for issue in receipt["issues"]))

    def test_invalid_inputs_do_not_launch(self):
        for extra in [("--timeout", "nan"), ("--timeout", "0"),
                      ("--resume", ""), ("--model", "--bad"),
                      ("--state-dir", str(SCRIPT.parent / "runtime-forbidden"))]:
            with self.subTest(extra=extra), tempfile.TemporaryDirectory() as root:
                prompt = Path(root) / "prompt"
                prompt.write_text("harmless")
                result = subprocess.run([sys.executable, "-B", str(SCRIPT),
                                         "--workspace", root, "--prompt-file", str(prompt),
                                         "--agent", "/nonexistent/cursor-test-agent",
                                         "--state-dir", str(Path(root) / "state"), *extra],
                                        capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertFalse((SCRIPT.parent / "runtime-forbidden").exists())

    @unittest.skipUnless(os.name == "posix", "POSIX signal forwarding")
    def test_sigterm_cancels_owned_child_and_records_receipt(self):
        source = '''import os, signal, time
os.kill(os.getppid(), signal.SIGTERM)
time.sleep(2)
open("escaped", "w").write("bad")
'''
        result, receipt, run_dir = self.invoke(source)
        self.assertEqual(result.returncode, 143)
        self.assertEqual(receipt["stop_reason"], "signal:15")
        self.assertEqual(receipt["transport_status"], "incomplete")
        self.assertFalse((run_dir.parent.parent / "escaped").exists())

    def test_invalid_utf8_and_missing_initialization_are_incomplete(self):
        for source, reason in [
            ('import sys; sys.stdout.buffer.write(b"\\xff\\n")', "malformed"),
            ('print(\'{"type":"result","subtype":"success","is_error":false,"session_id":"test-session"}\')', "initialization"),
        ]:
            with self.subTest(reason=reason):
                result, receipt, _ = self.invoke(source)
                self.assertEqual(result.returncode, 1)
                self.assertEqual(receipt["transport_status"], "incomplete")
                self.assertTrue(any(reason in issue for issue in receipt["issues"]))

    def test_argv_preserves_prompt_and_exact_policy(self):
        self.assertTrue(SCRIPT.exists(), "runner not implemented")
        spec = importlib.util.spec_from_file_location("cursor_run", SCRIPT)
        assert spec is not None and spec.loader is not None
        runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(runner)
        prompt = '--model bad; $(touch unwanted)\nquoted "text"'
        argv = runner.build_argv("agent", "/tmp/space here", prompt)
        self.assertEqual(argv, ["agent", "--print", "--output-format", "stream-json",
                               "--model", "cursor-grok-4.6-xhigh-fast", "--workspace",
                               "/tmp/space here", "--yolo", "--", prompt])
        argv = runner.build_argv("agent", "/tmp", prompt, model="exact-user-id",
                                 resume="exact-session", mode="ask", yolo=False)
        self.assertIn("exact-user-id", argv)
        self.assertEqual(argv[argv.index("--resume") + 1], "exact-session")
        self.assertEqual(argv[argv.index("--mode") + 1], "ask")
        self.assertNotIn("--yolo", argv)
        self.assertNotIn("--sandbox", argv)


if __name__ == "__main__":
    unittest.main()
