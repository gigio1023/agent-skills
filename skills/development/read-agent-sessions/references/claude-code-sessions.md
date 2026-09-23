# Claude Code Sessions

Verified against current Claude Code on this machine. CLI and desktop-app-launched sessions write to the same store; desktop sessions show `"entrypoint":"claude-desktop"` in their records.

## Storage

- Transcripts: `~/.claude/projects/<project-dir>/<session-uuid>.jsonl`, one JSON object per line. `<project-dir>` is the session cwd with `/` and `.` replaced by `-` (e.g. `-Users-suungho-park-git-personal-agent-skills-orch`). Reversing the dash encoding is ambiguous — read the `cwd` field from a record instead.
- Prompt history: `~/.claude/history.jsonl` with `{"display","timestamp","project","sessionId"}` per prompt — maps remembered fragments to session ids.
- Desktop app metadata: `~/Library/Application Support/Claude/claude-code-sessions/<org-uuid>/<user-uuid>/local_<uuid>.json` per session, carrying `sessionId` (the `local_*` id), **`cliSessionId`** (the `.jsonl` filename uuid), `cwd`, `title`, `titleSource`, `createdAt`, `lastActivityAt`, `model`, `isArchived`. This is the best title source for desktop sessions.
- `~/.claude/sessions/` is live IPC metadata, not transcripts. The Electron Local Storage leveldb is UI state, not a clean transcript source. claude.ai-side conversations live server-side; resume locally needs the id or URL, and local JSONL remains the reliable read source.

## Resolving an identifier

- Session id (uuid): `ls ~/.claude/projects/*/<uuid>.jsonl`
- Title: `grep -l 'custom-title.*<title>' ~/.claude/projects/*/*.jsonl` (the `custom-title` record appears as the first line of a session file), or grep the desktop metadata `"title"` and follow `cliSessionId`.
- Prompt fragment: `grep -F "<fragment>" ~/.claude/history.jsonl` for the session id.
- The widely documented `"type":"summary"` records did not exist in this machine's store; do not rely on them.

## Record schema

- First lines: meta records such as `{"type":"custom-title","customTitle":...}` and `{"type":"mode","mode":"normal",...}`.
- `type:"user"`: `message.content` is a string (real prompt) or an array containing `{"type":"tool_result",...}` blocks — tool results arrive as user-type records. `origin.kind=="human"` distinguishes real human turns; `isSidechain:true` marks subagent records.
- `type:"assistant"`: `message.content` array of `{"type":"thinking",...}` (skip), `{"type":"text","text":...}` (the readable output), and `{"type":"tool_use",...}` blocks.
- Every record carries `uuid`, `parentUuid`, `timestamp` (ISO 8601), `cwd`, `sessionId`, `version`, `gitBranch`.

## Extraction

```bash
jq -r '
  select(.type=="user" or .type=="assistant")
  | select(.isSidechain != true)
  | .timestamp as $t
  | .message.content
  | if type=="string" then "[\($t)] USER: \(.)"
    else (.[] | select(.type=="text") | "[\($t)] ASSISTANT: \(.text)")
    end' ~/.claude/projects/<dir>/<uuid>.jsonl
```

For human turns only, additionally filter user records on `.origin.kind=="human"`. Some sessions have a sibling `<session-uuid>/` directory next to the `.jsonl` holding subagent/worker data.

## CLI notes

`claude --resume <session-id>`, `claude --continue`, `--session-id`, `-n/--name`, `--fork-session`. `claude agents --json` prints the live interactive and background sessions as a JSON array without a TTY, and `--all` adds completed background sessions (confirmed on Claude Code 2.1.280, 2026-09-23). Past transcripts still need the filesystem. This skill only reads; resuming belongs to the harness.

## Caveats

- Thinking blocks are present but effectively empty locally; don't treat their absence as missing reasoning.
- Project-dir → path reversal is lossy; always use the `cwd` field.
- New record types may appear with versions; unknown types should be skipped, not interpreted.
