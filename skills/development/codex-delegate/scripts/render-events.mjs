#!/usr/bin/env bun
// render-events.mjs — compact, read-only renderer for `codex exec --json` logs.
//
// Usage:  bun render-events.mjs <events.jsonl> [--tail N]
//         bun render-events.mjs <events.jsonl> --status
// Also runs unchanged under `node` (>= 18); no runtime-specific APIs.
//
// Streams the log line by line, so a huge events.jsonl never lands in memory
// whole; with --tail N only N rendered lines are retained. One line per
// lifecycle event, 96-char cap on the assembled line. The payloads that make
// raw logs large (aggregated output, diff bodies, deltas) are never printed.
// Unknown or malformed vocabulary degrades to a marker instead of crashing.
//
// --status answers "is this run finished, working, or dead?" from the run
// directory's own files plus one liveness probe. Read-only throughout: the
// only non-read syscall is kill(-pgid, 0), which sends no signal and only
// asks whether the process group still exists.

import { createReadStream, readFileSync, statSync } from "node:fs";
import { createInterface } from "node:readline";

const MAX = 96;
const HUGE = 2000000; // never hand a line this long to JSON.parse
const CTRL = /[\u0000-\u001F\u007F-\u009F]/g; // ESC / OSC / BEL and friends

// Normalise and cap. Applied to individual fields and again to the assembled
// action line, so no rendered line can blow the width budget or smuggle
// terminal escape sequences out of a log.
function shorten(text) {
  const s = String(text ?? "").replace(CTRL, " ").replace(/\s+/g, " ").trim();
  return s.length <= MAX ? s : `${s.slice(0, MAX - 1)}…`;
}

function isObject(value) {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

// Last path segment only — absolute paths would eat the whole line budget.
function basename(path) {
  const s = String(path ?? "").replace(/[/\\]+$/, "");
  return s.split(/[/\\]/).pop() || "?";
}

// --- status helpers: every one of these degrades to null rather than throw,
// so a half-written run directory still produces a readable verdict.

function fileStat(path) {
  try {
    return statSync(path);
  } catch {
    return null;
  }
}

function size(path) {
  const s = fileStat(path);
  if (!s) return "—";
  if (s.size < 1024) return `${s.size}B`;
  if (s.size < 1048576) return `${Math.round(s.size / 1024)}KB`;
  return `${(s.size / 1048576).toFixed(1)}MB`;
}

function elapsed(ms) {
  if (ms == null || !Number.isFinite(ms)) return "?";
  const s = Math.max(0, Math.round(ms / 1000));
  if (s < 60) return `${s}s`;
  const m = Math.floor(s / 60);
  if (m < 60) return `${m}m${String(s % 60).padStart(2, "0")}s`;
  return `${Math.floor(m / 60)}h${String(m % 60).padStart(2, "0")}m`;
}

// Signal 0 sends nothing. A negative pid targets the process group, which is
// what the detached launcher records. EPERM means it exists but is not ours.
function groupAlive(pgid) {
  if (!Number.isInteger(pgid) || pgid <= 1) return null;
  try {
    process.kill(-pgid, 0);
    return true;
  } catch (error) {
    return error.code === "EPERM";
  }
}

function collabSnapshot(item) {
  const receivers = Array.isArray(item.receiver_thread_ids)
    ? item.receiver_thread_ids.map(String)
    : [];
  const states = isObject(item.agents_states) ? item.agents_states : {};
  const counts = new Map();
  for (const state of Object.values(states)) {
    const status = isObject(state) ? state.status : state;
    const key = shorten(status ?? "unknown") || "unknown";
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return {
    receivers,
    states,
    total: Math.max(receivers.length, Object.keys(states).length),
    summary: [...counts.entries()]
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([name, count]) => `${name} ${count}`)
      .join(", "),
  };
}

// `item.updated` renders nothing, for every item type: `started` (▶) and
// `completed` (✓) already carry the signal, updates only add deltas and
// partial text, and a ✓ on an in-progress item would read as finished.
function describeItem(item, lifecycle) {
  if (lifecycle === "updated") return null;
  const mark = lifecycle === "started" ? "▶" : "✓";
  const done = lifecycle === "completed";
  switch (item.type) {
    case "command_execution":
      if (lifecycle === "started") return `▶ $ ${shorten(item.command)}`;
      if (!done) return null;
      return `✓ exit ${item.exit_code ?? "?"} · $ ${shorten(item.command)}`;
    case "file_change": {
      const list = Array.isArray(item.changes) ? item.changes : [];
      const count = Array.isArray(item.changes) ? list.length : "?";
      const names = list
        .slice(0, 5)
        .map((c) => basename(isObject(c) ? c.path : c))
        .join(" ");
      return `${mark} file_change ×${count} ${names}`;
    }
    case "agent_message":
      return done ? `✉ ${shorten(item.text)}` : null;
    case "reasoning": {
      if (!done) return null;
      const first = String(item.text ?? item.summary ?? "").split("\n")[0];
      return first ? `· ${shorten(first)}` : null;
    }
    case "mcp_tool_call":
      return `${mark} mcp ${shorten(item.server ?? "?")}/${shorten(item.tool ?? "?")} ${shorten(item.status ?? "")}`;
    case "collab_tool_call": {
      const snapshot = collabSnapshot(item);
      const agents = snapshot.total
        ? ` · ${snapshot.total} agent${snapshot.total === 1 ? "" : "s"}`
        : "";
      const states = snapshot.summary ? `: ${snapshot.summary}` : "";
      return `${mark} collab ${shorten(item.tool ?? "?")}${agents}${states}`;
    }
    case "web_search": {
      // `query` is empty on `started`, and stays empty on `completed` for a
      // multi-query search — the terms live in `action.queries` instead.
      const action = isObject(item.action) ? item.action : {};
      const queries = Array.isArray(action.queries) ? action.queries : [];
      const count = queries.length > 1 ? ` ×${queries.length}` : "";
      return `${mark} search${count} ${shorten(item.query || queries[0] || "")}`;
    }
    case "error":
      return `⚠ ${shorten(item.message)}`;
    default:
      return `${mark} ${shorten(item.type ?? "unknown_item")}`;
  }
}

function describeEvent(event) {
  switch (event.type) {
    case "thread.started":
      return `thread ${shorten(event.thread_id)}`;
    case "turn.started":
      return null;
    case "item.started":
    case "item.updated":
    case "item.completed":
      return isObject(event.item)
        ? describeItem(event.item, event.type.slice(5))
        : "? malformed event";
    case "turn.completed": {
      const u = isObject(event.usage) ? event.usage : {};
      return `turn done · tokens in ${u.input_tokens ?? "?"} (cached ${u.cached_input_tokens ?? 0}) out ${u.output_tokens ?? "?"}`;
    }
    case "turn.failed":
      return `✗ turn failed · ${shorten(isObject(event.error) ? event.error.message : "")}`;
    case "error":
      return `✗ ${shorten(event.message)}`;
    default:
      return event.type ? `? ${shorten(event.type)}` : "? malformed event";
  }
}

const args = process.argv.slice(2);
const tailIndex = args.indexOf("--tail");
const tail = tailIndex >= 0 ? Number(args[tailIndex + 1]) : null;
const status = args.includes("--status");
// Skip the value that belongs to --tail, so `--tail 20 events.jsonl` still
// resolves the file rather than treating "20" as the path.
const file = args.find((a, i) => !a.startsWith("--") && (tailIndex < 0 || i !== tailIndex + 1));
if (!file || (tailIndex >= 0 && (!Number.isInteger(tail) || tail <= 0))) {
  console.error("usage: render-events.mjs <events.jsonl> [--tail N | --status]");
  process.exit(2);
}

const kept = []; // bounded ring buffer: at most `tail` rendered lines
const inFlight = new Map(); // item id -> its ▶ line, cleared on completion
let omitted = 0;
let threadId = null;
let events = 0;
let commands = 0;
let fileChanges = 0;
let unparseable = 0;
let streamError = null;
const observedAgents = new Map(); // receiver thread id -> last root-visible status

function emit(line) {
  kept.push(shorten(line));
  if (tail && kept.length > tail) {
    kept.shift();
    omitted += 1;
  }
}

const rl = createInterface({ input: createReadStream(file), crlfDelay: Infinity });
try {
  for await (const line of rl) {
    if (!line.trim()) continue;
    events += 1;
    if (line.length > HUGE) {
      unparseable += 1;
      emit("? oversized event line");
      continue;
    }
    let event;
    try {
      event = JSON.parse(line);
    } catch {
      unparseable += 1;
      emit("? unparseable line");
      continue;
    }
    if (!isObject(event)) {
      emit("? malformed event");
      continue;
    }
    const item = isObject(event.item) ? event.item : null;
    if (event.type === "thread.started" && event.thread_id) threadId = event.thread_id;
    if (event.type === "item.completed" && item?.type === "command_execution") commands += 1;
    if (event.type === "item.completed" && item?.type === "file_change") fileChanges += 1;
    if (item?.type === "collab_tool_call") {
      const snapshot = collabSnapshot(item);
      for (const id of snapshot.receivers) {
        if (!observedAgents.has(id)) observedAgents.set(id, "unknown");
      }
      for (const [id, state] of Object.entries(snapshot.states)) {
        const value = isObject(state) ? state.status : state;
        observedAgents.set(id, shorten(value ?? "unknown") || "unknown");
      }
    }
    const rendered = describeEvent(event);
    if (item && item.id != null) {
      if (event.type === "item.started") inFlight.set(item.id, rendered);
      if (event.type === "item.completed") inFlight.delete(item.id);
    }
    if (rendered) emit(rendered);
  }
} catch (error) {
  // A run that has not written its first event yet is a normal status case;
  // for rendering there is nothing to show, so it stays fatal there.
  streamError = error.message;
  if (!status) {
    console.error(`cannot read ${file}: ${error.message}`);
    process.exit(1);
  }
}

if (status) {
  const runDir = file.replace(/[/\\][^/\\]*$/, "") || ".";
  const result = (() => {
    try {
      return readFileSync(`${runDir}/result.txt`, "utf8").split("\n");
    } catch {
      return [];
    }
  })();
  const provenance = result[0] ?? "";
  const terminal = result.find((l) => /^(exit|cancelled|cancel_failed)=/.test(l)) ?? null;
  const handoff = (terminal?.match(/\bhandoff=(ready|incomplete)\b/) ?? [])[1] ?? null;
  const pgid = Number((provenance.match(/\bpgid=(\d+)/) ?? [])[1]);
  const startedAt = Date.parse((provenance.match(/\bstarted=(\S+)/) ?? [])[1] ?? "");
  const age = Number.isFinite(startedAt) ? Date.now() - startedAt : null;
  const alive = terminal ? null : groupAlive(pgid);
  const eventStat = fileStat(file);

  let state;
  let hint = null;
  if (terminal && terminal.startsWith("exit=")) {
    const exit = terminal.split(/\s+/)[0];
    if (terminal.startsWith("exit=0") && handoff === "incomplete") {
      state = `INCOMPLETE ${exit} handoff=incomplete`;
      hint = "codex exited cleanly but report.md is empty or missing. Inspect the last agent message, then resume for a file handoff.";
    } else if (terminal.startsWith("exit=0")) {
      state = `DONE ${exit}${handoff ? ` handoff=${handoff}` : ""}`;
      hint = handoff === "ready"
        ? "file handoff is ready. Verify the workspace yourself before trusting the report."
        : "legacy terminal line has no handoff marker. Check report.md before trusting it.";
    } else {
      state = `EXITED ${exit}${handoff ? ` handoff=${handoff}` : ""}`;
      hint = "codex exited non-zero. Read stderr.log and classify the failure before resuming the exact thread; do not retry automatically.";
    }
  } else if (terminal) {
    state = terminal.split("=")[0].toUpperCase();
  } else if (alive === true) {
    state = "RUNNING";
  } else if (alive === false) {
    state = "DIED";
    hint = "no terminal line and the process group is gone: it was killed, not finished. The files above are whatever it had written; resume the thread rather than starting over.";
  } else {
    state = "UNKNOWN";
    hint = "no terminal line and no pgid to probe — this run predates the durable template, or result.txt is truncated.";
  }

  const line2 = [`state    ${state}`];
  if (Number.isInteger(pgid) && pgid > 1) line2.push(`pgid ${pgid}${alive === false ? " gone" : ""}`);
  if (age != null) line2.push(`started ${elapsed(age)} ago`);

  const stream = [`${events} events`];
  if (eventStat) stream.push(`last write ${elapsed(Date.now() - eventStat.mtimeMs)} ago`);
  else if (streamError) stream.push("no events.jsonl yet");
  const pending = [...inFlight.values()].filter(Boolean);
  if (pending.length) stream.push(`in flight ${shorten(pending[pending.length - 1])}`);

  console.log(`run      ${basename(runDir)}`);
  console.log(line2.join(" · "));
  console.log(`stream   ${stream.join(" · ")}`);
  console.log(
    `files    report.md ${size(`${runDir}/report.md`)} · stderr.log ${size(`${runDir}/stderr.log`)}`,
  );
  if (observedAgents.size) {
    const counts = new Map();
    for (const value of observedAgents.values()) {
      counts.set(value, (counts.get(value) ?? 0) + 1);
    }
    const summary = [...counts.entries()]
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([name, count]) => `${name} ${count}`)
      .join(", ");
    console.log(`agents   partial root snapshot · ${observedAgents.size} observed · ${summary}`);
  }
  if (threadId) console.log(`thread   ${shorten(threadId)}`);
  if (hint) console.log(`next     ${hint}`);
} else {
  if (omitted) console.log(`… ${omitted} earlier line(s) omitted`);
  for (const line of kept) console.log(line);

  let footer = `— ${events} events · ${commands} commands · ${fileChanges} file-changes`;
  if (threadId) footer += ` · thread ${shorten(threadId)}`;
  if (unparseable) footer += ` · ${unparseable} unparseable`;
  console.log(footer);
}
