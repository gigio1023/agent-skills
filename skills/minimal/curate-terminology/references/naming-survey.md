# Naming Survey

## Source classes

| Class | Read | Gives |
| --- | --- | --- |
| Established projects | Official docs, API reference, maintainer blog posts, source | Developer usage and exact identifiers |
| Papers | The defining paper, widely cited follow-ups and surveys, author or lab explanations | Research usage and formal meaning |
| Competitor products | Product docs, API reference, changelogs | The names this market's customers see |

Pick sources the project's readers would recognize: wide adoption, sustained maintenance, use as a baseline, or citation in primary work. Stars, search rank, and polished prose are not enough. A paper's method name is that paper's usage, not a field standard. A competitor's marketing page shows the name customers see; take its meaning from the product docs. A class with nothing to say about the concept is skipped.

## Source quality

AI-generated derivative prose, such as synthetic tutorials, automated paper summaries, and content-farm explainers, is not an authority for a name, even on a familiar platform. Follow its links to a primary source or skip it. AI-tooling projects get extra scrutiny: the user named `opencodex` and `oh my claude code` as examples of documentation whose coined labels should not be adopted without support from established sources or the implementation. A compound label that maps to no concrete behavior, a renamed ordinary operation, or a circular definition disqualifies the passage. Authorship is not judged from style alone.

## Reading

Read the passage where the source defines or uses the name, not a search snippet or abstract. Note the version or check date for products whose naming changes. For papers, `literature-research` in research-credo handles search, reading, and saved copies; the glossary needs only the citation and the passage locator.

## Settling a split

- Different names, same meaning: adopt the name used by the ecosystem the project's readers work in, usually the majority of the surveyed sources. List the others under Elsewhere called.
- Same name, different meanings: keep the meaning the project uses and list the other meanings with their source, for example `OpenTelemetry: trace = linked spans of one request`.
- A local or user-decided name overrides field usage for this project only. The row still lists the field's name so readers can map between them.
