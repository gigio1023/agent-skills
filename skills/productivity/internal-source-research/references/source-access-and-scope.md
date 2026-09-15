# Source Access and Scoped Retrieval

Use this reference when deciding which source lanes to inspect, checking an access failure, or explaining why a result is incomplete. It describes a read-only research method, not a way to obtain access.

## Start from a narrow evidence plan

Write down the question, relevant containers or objects, workstreams, time boundary, and the reason each service might answer it. A source becomes eligible because it is in the user's scope or can answer the bounded question—not merely because its connector is visible.

Start with named anchors and nearby context. Do not make a workspace-wide export, broad repository harvest, direct-message sweep, or search across unrelated teams by default. A source document may point to another object, but that only justifies a follow-up when it remains within the approved frame.

## Discover the relevant plugin or MCP route

Start with appropriate tools already exposed in the session. When a source lane is missing or unclear, use the host's documented tool discovery and plugin inventory or catalog if available. For MCP, inspect safe server status and tool listings through supported interfaces. A tools-only MCP server may expose no resources: an empty resource list says nothing by itself about its tools or connection. A plugin may be discoverable in a catalog without being installed, or installed without being enabled or connected in this session.

Inspect only services relevant to the question. For each requested Notion, GitHub, Linear, or Slack lane, establish the usable access route or name the unresolved state. Do not infer that a plugin or server is absent merely because its tools are not currently visible. If inventory or discovery is unavailable, say availability is unverified and continue the usable lanes.

Use status and metadata interfaces without dumping raw configuration, tokens, environment variables, or authentication stores. Do not invent plugin identifiers, MCP server names, commands, or flags. Installing a plugin, starting an unreviewed MCP command, connecting an account, and changing configuration or permissions are setup actions, not read-only discovery. Leave them as a specific prerequisite unless the user authorizes setup.

## Distinguish access states

| Condition | What to establish through a safe scoped operation | What it does not establish |
| --- | --- | --- |
| Catalog availability | A suitable integration is discoverable in the host's supported catalog. | Installation, configuration, or permission to use it. |
| Installation or configuration | A plugin is installed or an MCP server is configured, as reported by a safe metadata interface. | Enablement, connection, or session tool exposure. |
| Connection and tool exposure | A suitable reader is connected and its needed tools can be invoked in this session. | Authentication, target permission, or readable content. |
| Authentication | The reader reports an active account or accepts a harmless request without exposing a token. | Permission to the target container. |
| Read authorization | The current identity can discover or open the scoped container or object. | That decisive content, history, replies, or revisions can be retrieved. |
| Content retrieval | The actual needed object returns enough readable content and a usable locator for evaluation. | That the source is complete, current, or corroborated. |

These are independent observations, not a compulsory sequence of six requests. An actual scoped read may establish several states at once without revealing how the integration was installed. Record only what the operation establishes; do not guess from a generic error. Lead and delegated workers establish their own relevant access, reusing valid session evidence where available; one principal's success is not another's evidence.

Honor a user-selected plugin, MCP, or other access route. A service CLI or browser may use a different identity or expose a broader scope; it is a fallback only when allowed and its scoped access is established. An empty tool-discovery result is not permission to switch channels or authenticate a different account.

## Service-shaped checks

Use the service's native concepts without assuming an API or a particular connector.

- **Notion:** distinguish discovery of a page or database from permission to its page contents, linked pages, and relevant history. A search preview is not a full document read.
- **Slack:** scope channels deliberately and distinguish a message hit from readable thread replies, adjacent context, and allowed channel history. Do not broaden to direct messages unless explicitly authorized.
- **GitHub:** distinguish organization or repository discovery from readable issues, pull requests, revisions, code, discussions, and the exact branch or diff needed for the claim.
- **Linear:** distinguish team or project discovery from readable issue state, issue history, comments, and the filters that shaped a query. An empty filtered view is only evidence about that view.

For another service, use the same distinction: discovery, authorization, and complete enough retrieval are separate observations.

## Interpret absence carefully

An empty result may reflect a narrow query, indexing delay, retention, an inaccessible container, a time filter, a different vocabulary, a pagination boundary, a partial result, or actual absence in the searched slice. Before treating it as absence, check whether the reader exposes more pages, a result ceiling, archive or retention behavior, or an incomplete retrieval status. Record that coverage boundary; do not enumerate every page when the bounded question is already answered.

Use relevant aliases, renamed workstreams, acronyms, or adjacent terms when an initial label could conceal decisive evidence. Add terms only when they can change the answer, and keep them within the approved source and time scope. Do not turn synonym expansion into an exhaustive vocabulary sweep.

Treat an authorization or retrieval failure as coverage information. Continue with another authorized lane, look for an in-scope primary source, or leave the question unknown. Ask for a broader scope or access change only when the missing lane is necessary to the decision.

## Preserve provenance without over-sharing

For a material finding, retain the source-native object type and locator, relevant artifact date, observation date, and the bounded source scope in approved storage. Cite the original artifact when the audience may receive that locator. Private URLs, workspace names, account identifiers, and quoted personal details can disclose information even without a document body. Omit incidental identifiers and redact sensitive URL components from shared diagnostics; retain the necessary original provenance only in the authorized private record. If redaction makes a citation unusable, describe the access limit rather than presenting a broken locator as verifiable evidence.

Summarize only the portion needed to support the claim and follow the task's sharing and retention limits. An approved worker handoff may include the minimum permitted excerpt or source output needed to establish the claim on the same authorized surface; it must not include credentials or a raw private corpus. Neither a cheaper model nor a requested summary expands the approved audience or provider. No live data belongs in a reusable skill.
