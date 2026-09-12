# Hermes Sessions

Verified by direct query against this machine's database. Hermes Agent is a Python harness (`~/.local/bin/hermes`); the canonical store is SQLite.

## Storage

- Database: `~/.hermes/state.db` (large, live, WAL-backed — open read-only: `sqlite3 "file:$HOME/.hermes/state.db?mode=ro"`). Tables: `sessions`, `messages`, `messages_fts` (FTS5), `messages_fts_trigram`, `session_model_usage`, `gateway_routing`.
- `~/.hermes/sessions/` is NOT transcripts despite the name — it holds `request_dump_*.json` and a legacy `sessions.json` mirror of the `gateway_routing` index. Don't read it for conversations.

## Session identity

- Id format: `YYYYMMDD_HHMMSS_<6-hex>` (start-time based), e.g. `20260910_231100_9b57d3`.
- `sessions` columns: `id`, `title` (often NULL; when set, a human/auto title), `display_name`, `source` (`cli`/`tui`/`desktop`/`discord`/`subagent`/`tool`/cron names), `started_at`/`ended_at` (unix REAL), `message_count`, `cwd`, `model`, `parent_session_id`, `archived`/`pinned`/`hidden`.

## Resolving an identifier

```bash
# by id, title, or display name
sqlite3 "file:$HOME/.hermes/state.db?mode=ro" \
  "select id, title, datetime(started_at,'unixepoch','localtime'), message_count
   from sessions where id like '%<frag>%' or title like '%<keywords>%'
      or display_name like '%<keywords>%';"

# no title? use the first user message as the identifier
sqlite3 "file:$HOME/.hermes/state.db?mode=ro" \
  "select s.id, (select substr(content,1,80) from messages m
                 where m.session_id = s.id and m.role='user'
                 order by m.timestamp limit 1)
   from sessions s order by s.started_at desc;"
```

Full-text search across all messages uses `messages_fts`; substring search for non-tool messages uses `messages_fts_trigram`.

## Record schema and extraction

`messages` columns: `session_id`, `role` (`user`/`assistant`/`tool`), `content`, `tool_calls`/`tool_call_id`/`tool_name`, `timestamp` (unix REAL), `token_count`, `finish_reason`, `active`/`compacted`/`_compressed_summary`, `display_order`.

```bash
sqlite3 "file:$HOME/.hermes/state.db?mode=ro" \
  "select datetime(timestamp,'unixepoch','localtime'), role,
          substr(coalesce(content,''),1,400)
   from messages
   where session_id='<id>' and active=1
   order by timestamp, id;"
```

Exclude `role='tool'` and `active=0`/`compacted=1` rows for a human-readable conversation. Duplicate rows with identical timestamps occur (regeneration/rewind artifacts) — dedupe by content + timestamp before summarizing.

## CLI alternative

`hermes sessions list`, `hermes sessions export` (JSONL / Markdown / QMD), `hermes sessions rename` — read-only viewing via these is safe and often faster than SQL.

## Caveats

- Gateway/platform conversations (Discord etc.) may need the `gateway_routing` table to map a chat key to a session id.
- Backup files `state.db.pre-update-emergency-*.bak` are stale snapshots; use the live DB.
