# Anti-Slop Research

Use this when subagents search the web, GitHub, papers, blogs, agent-skill
collections, product docs, or community examples.

## Source Quality Signals

Strong signals:

- Official documentation, standards, release notes, papers, or source code.
- Repos with clear maintainers, tests, issues, releases, and real examples.
- Claims that can be verified by running code, inspecting files, or checking
  primary artifacts.
- Writing that names trade-offs and limitations.

Weak signals:

- Generic "awesome" collections with no curation criteria.
- High star counts with suspicious recency, thin commits, or marketing-heavy
  descriptions.
- Blog posts that repeat product claims without examples.
- Agent-skill collections that promise hundreds of skills but provide shallow
  wrappers, duplicated prompts, or no validation path.
- AI-generated articles with generic phrasing, no source trail, and no concrete
  operational detail.

## Popularity Is Not Proof

Use stars, forks, package downloads, citations, and social traction as adoption
signals only. They do not prove correctness, maintainability, or fit.

For tools and skills, inspect:

- Last meaningful commit and release cadence.
- Issue quality and maintainer response.
- Whether examples are executable.
- Whether the design matches the user's actual harness.
- License and installation risk.
- Whether the repo distinguishes policy from implementation detail.

## Assign Anti-Slop Lanes

For high-noise topics, dedicate one subagent to skepticism:

- Find source inflation, copied text, fake curation, outdated claims, and
  unsupported hype.
- Compare public claims against actual files.
- Identify which artifacts are worth ignoring.

The skeptic does not need to be negative. The useful output is calibrated trust.

## Research Output Contract

Every research lane should return:

- Sources inspected.
- Which sources were discarded and why.
- Claims supported by direct evidence.
- Claims that are plausible but unverified.
- Currentness/date boundary.
- Recommendation for adoption, rejection, or follow-up.
