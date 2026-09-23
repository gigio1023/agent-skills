# Codex Sessions

Verified against codex-cli 0.153–0.154 on this machine. The CLI and the Codex desktop app share one store, so a single lookup route covers both; a session's `session_meta.originator` says which surface created it (`"Codex Desktop"` or a CLI value).

## Storage

- Transcripts: `~/.codex/sessions/YYYY/MM/DD/rollout-<ISO-timestamp-with-dashes>-<session-uuid>.jsonl`, one JSON object per line. The filename timestamp is local time; record timestamps inside are UTC ISO 8601.
- Title index: `~/.codex/session_index.jsonl`, one line per update: `{"id":"<uuid>","thread_name":"<title>","updated_at":"<iso>"}`. Multiple lines per id are normal — the latest line wins. Titles are often derived from the first user message, including non-English text verbatim.
- Prompt history: `~/.codex/history.jsonl` with `{"session_id","ts","text"}` per user prompt — useful for mapping a remembered prompt fragment to a session id.
- Archived transcripts: `codex archive` moves a rollout to `~/.codex/archived_sessions/` with the same file-name scheme, and `codex unarchive` moves it back. A lookup by id must search both directories.
- Thread-history store: Codex 0.154.0 also keeps `~/.codex/thread_history_1.sqlite` and ships `codex migrate-rollouts`, which moves legacy sessions into that paginated store. On 2026-09-23 new rollouts still landed in `sessions/`; if they stop appearing there, recheck this reference before relying on the JSONL route.
- `~/Library/Application Support/Codex/` holds the app's Chromium profile and artifact runtime, not transcripts. Ignore it for reading conversations.

Session id is a UUIDv7; it equals the trailing UUID of the filename and the `payload.id` of the first `session_meta` line. Subagent sessions are separate rollout files whose `session_meta` carries `parent_thread_id` (and `source` spawn info); follow them when delegated work matters.

## Resolving an identifier

- Session id or prefix: `find ~/.codex/sessions ~/.codex/archived_sessions -name "*<id-prefix>*.jsonl"`
- Title: `grep '"thread_name":"<title>"' ~/.codex/session_index.jsonl` — take the last matching line's `id`, then find the file by that id.
- Prompt fragment: `grep -F "<fragment>" ~/.codex/history.jsonl` for the session id, or grep the `thread_name` values in the index.

## Record schema

Every line: `{"timestamp","ordinal","type","payload"}`. Relevant `type` values:

- `session_meta` (line 1): session id, `parent_thread_id`, `cwd`, `originator`, `cli_version`, model provider, base instructions, spawn info.
- `response_item` — the authoritative transcript. `payload.type`:
  - `message` with `role`: `user` (real human turns), `developer` (injected context such as plugin lists — exclude), `assistant` (model output). Content is an array of `{"type":"input_text"|"output_text","text":...}`.
  - `reasoning` (reasoning summaries; some are `encrypted_content` and unreadable locally).
  - `custom_tool_call` / `custom_tool_call_output` — tool activity.
  - `agent_message` — inter-agent communication, often encrypted.
- `event_msg` — UI/streaming events (`item_completed`, `token_count`, ...). These duplicate `response_item` content; do not use them for the transcript.
- `turn_context`, `world_state`, `token_usage_record` — auxiliary.

## Extraction

```bash
jq -r 'select(.type=="response_item" and .payload.type=="message")
       | .timestamp + " " + .payload.role + ": " +
         (.payload.content | map(.text // empty) | join(""))' "$F"
```

Filter out `role=="developer"` for the user-visible conversation; add `custom_tool_call` records when tool detail is requested.

## Caveats

- Older Codex versions wrote the same directory layout but without `session_index.jsonl` and with fewer payload types; title lookup by index fails there — fall back to first-user-message grep.
- Assistant reasoning and inter-agent messages may be encrypted and unreadable; note the gap instead of inferring their content.
