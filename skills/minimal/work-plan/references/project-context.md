# Project Context

Keep a project's purpose, direction, constraints, current understanding, next important question, and resource locations available to later sessions. A project is an objective, not necessarily a Git repository: its code, data, experiments, documents, and live jobs may span several locations. This reference carries the duty of the retired `gigio-project-setup`.

Use it when a plan spans repositories or sessions and no instruction file or maintained intent document already carries that context, or when the user asks to record or audit it. Sufficient existing context does not need this pass again. No particular file is required: a plan links whatever intent documents exist in its goal and basis.

## Recover before writing

Inspect existing intent documents, project instructions, relevant decisions, current results, and resource locations. Reuse an equivalent maintained document instead of introducing a competing record; an existing `PROJECT.md` from earlier work is such a document and stays where it is. Ask only for missing user judgments that change the record materially.

Separate user decisions from observations and agent proposals. Preserve the user's wording for goals and important limits; a synthesis may connect those statements without upgrading an inference into consent. Do not require a failure anecdote, a fixed number of pillars, or a negated definition for each goal.

## Write the smallest useful record

When nothing carries the context, write one short record at the root the plans live under, named to fit the project's conventions, link it from the plan's goal and basis, and report its path. It holds two kinds of content:

- **User-owned direction:** why the work matters, the question or outcome pursued, priorities, meaningful exclusions, constraints, and the choices the user has settled. Mark this section; a change needs the user's decision, and a grant already given does not need repeating.
- **Maintained understanding:** what the work currently supports, important competing explanations, what is not established, abandoned approaches and why, the next decision, and links to the results that matter. Update it during authorized work without asking the user to approve each observation. Findings can challenge a decision; they do not silently replace it.

Give each material decision a concise reason and its source, and supersede outdated entries rather than letting an old result look current. Record uncertainty where it affects the next action, not as a label on every sentence.

Map code, datasets, experiment records, documents, and remote resources only as needed to retrieve them. Reuse existing run registries, research indexes, and notebooks, and link raw results instead of copying them; the record is not a second experiment database.

State how progress is assessed: a working capability, a defensible finding, an excluded explanation, an evaluated dataset, a useful artifact, or a documented limit on what can be concluded. Test and lint requirements belong here when they apply to the project's implementation.

## Connect later sessions

Wire the record into the project's instruction entry points, such as `AGENTS.md` or `CLAUDE.md`, only when the user asked for that wiring. Preserve unrelated instructions, and where the project uses both files keep its own bridge between them rather than promising that every harness reads one of them. A multi-repository project can keep its record at an agreed workspace or research root and link it from participating repositories. When the project keeps a terminology index, link it rather than copying definitions; the `terminology` skill owns its instruction snippet. An audit reports missing or stale wiring without changing it.

## Check that it persists

Check that the next session can locate the record, retrieve the decisive sources, and tell established direction from current hypotheses, comparing the digest with actual results and live state where relevant. Git is one persistence mechanism: an uncommitted file is not automatically invalid, and a commit alone does not make a record reachable on another machine. Check the actual storage, synchronization, access, and retention arrangements.
