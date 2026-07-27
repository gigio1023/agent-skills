#!/usr/bin/env bun
// render-events.mjs — compact, read-only renderer for `codex exec --json` logs.
//
// Usage:  bun render-events.mjs <events.jsonl> [--tail N]
// Also runs unchanged under `node` (>= 18); no runtime-specific APIs.
//
// Streams the log line by line, so a huge events.jsonl never lands in memory
// whole; with --tail N only N rendered lines are retained. One line per
// lifecycle event, 96-char cap on the assembled line. The payloads that make
// raw logs large (aggregated output, diff bodies, deltas) are never printed.
// Unknown or malformed vocabulary degrades to a marker instead of crashing.
// Read-only: it never manages processes or state.

import { createReadStream } from "node:fs";
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
const file = args.find((a) => !a.startsWith("--"));
const tailIndex = args.indexOf("--tail");
const tail = tailIndex >= 0 ? Number(args[tailIndex + 1]) : null;
if (!file || (tailIndex >= 0 && (!Number.isInteger(tail) || tail <= 0))) {
  console.error("usage: render-events.mjs <events.jsonl> [--tail N]");
  process.exit(2);
}

const kept = []; // bounded ring buffer: at most `tail` rendered lines
let omitted = 0;
let threadId = null;
let events = 0;
let commands = 0;
let fileChanges = 0;
let unparseable = 0;

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
    const rendered = describeEvent(event);
    if (rendered) emit(rendered);
  }
} catch (error) {
  console.error(`cannot read ${file}: ${error.message}`);
  process.exit(1);
}

if (omitted) console.log(`… ${omitted} earlier line(s) omitted`);
for (const line of kept) console.log(line);

let footer = `— ${events} events · ${commands} commands · ${fileChanges} file-changes`;
if (threadId) footer += ` · thread ${shorten(threadId)}`;
if (unparseable) footer += ` · ${unparseable} unparseable`;
console.log(footer);
