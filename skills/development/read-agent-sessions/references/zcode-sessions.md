# Zcode Sessions

Verified by direct query against this machine's database. All conversational data lives in SQLite; there is no JSONL store.

## Storage

- Database: `~/.zcode/cli/db/db.sqlite` (with `-wal`/`-shm` — the live WAL is large, so recent turns may not be in the main file yet). Read it with the sqlite3 CLI; do not copy the files, and open read-only:
  `sqlite3 "file:$HOME/.zcode/cli/db/db.sqlite?mode=ro"`
- Tool-call results: `~/.zcode/cli/artifacts/sess_*/call_<id>-tool-result-<uuid>.json` — referenced by call id, not inlined in the DB.
- `~/.zcode/v2/tasks-index.sqlite` is a background-task index, not conversations. `~/.zcode/cli/rollout/` exists but was empty; don't depend on it.

## Session identity

- Interactive/main sessions: `sess_<uuid>`.
- Subagent sessions: `sess_subagent_agent_<uuid>` with `parent_id` pointing at the parent session row.

The `session` table has one row per conversation: `id`, `title` (auto-generated from the first input or custom), `title_source`, `directory` (project path), `parent_id`, `task_type`, `time_created`/`time_updated` (ms epoch), `version`.

## Resolving an identifier

```bash
sqlite3 "file:$HOME/.zcode/cli/db/db.sqlite?mode=ro" \
  "select id, title, directory, datetime(time_updated/1000,'unixepoch')
   from session order by time_updated desc;"
```

Match on `id` (a `sess_` prefix or full uuid), or on `title` / `directory` for a title- or project-based lookup.

## Record schema

- `message(id, session_id, time_created, sequence, data JSON)` — one row per turn. `data` carries `role` (`user`/`assistant`), `modelID`, `path.cwd`, and `semantics` with `origin` (`real_user`/`system`) and `kind` (`user_prompt`/`timeline_event`).
- `part(id, message_id, session_id, sequence, data JSON)` — content fragments. `data.type=="text"` with a `text` field is the readable prose; `type:"timeline"` rows are model-change and similar events.

## Extraction

```bash
sqlite3 -json "file:$HOME/.zcode/cli/db/db.sqlite?mode=ro" "
select m.sequence, json_extract(m.data,'$.role') as role, p.data as part
from message m join part p on p.message_id = m.id
where m.session_id = '<sess_id>'
  and json_extract(p.data,'$.type') = 'text'
order by m.sequence, p.sequence;" \
| jq -r '.[] | "## " + .role + "\n" + (.part | fromjson | .text)'
```

Filter `json_extract(m.data,'$.semantics.origin') = 'real_user'` on user rows to skip system-injected input. For tool results, take call ids from the conversation and read the matching artifacts JSON files.

## Caveats

- The DB is live and WAL-backed; always `mode=ro` and expect very recent turns in the WAL.
- No verified `zcode` CLI resume/list surface was available at verification time; rely on the database.
