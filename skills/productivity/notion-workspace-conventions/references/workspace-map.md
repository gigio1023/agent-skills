# Workspace Map

Durable destinations in this user's Notion workspace, recorded by role. Resolve every new page's parent from this table before creating it.

| Role | Destination | Rule |
| --- | --- | --- |
| Standalone documents | "문서 모음" database | Fetch the database first; use its data source ID and exact property names for rows |
| Project research and investigations | The project's hub page | Create as a child of the hub; link the page back from the hub once |
| Throwaway notes | Scratchpad (private) | Never linked from other pages; never a destination for durable content |
| Meeting records | Unmapped — ask first | Confirm the parent page with the user before creating |
| Decision records | Unmapped — ask first | Confirm the parent page with the user before creating |

## Maintenance

Entries live in the agent-skills repository, not in installed copies. When the user confirms a new durable destination, add the row there so future sessions inherit it, and remove rows whose role has moved.
