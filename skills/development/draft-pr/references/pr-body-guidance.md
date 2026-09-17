# PR Body Guidance

Read this when a repository has no PR template or when deciding whether a change needs optional reviewer context. Repository templates remain authoritative even when their headings differ from this fallback.

## Contents

- Reader test
- Default shape
- Conditional sections
- Validation
- Writing rules
- Pattern basis

## Reader Test

A useful PR body lets a reviewer or future maintainer answer:

- What problem or constraint led to this change?
- What reviewer-visible outcomes does the branch introduce?
- What important decision, boundary, risk, or user impact is absent from the diff?
- What needs human review that CI cannot prove?

The title should describe the whole diff in one specific sentence. If it cannot, surface a scope mismatch; a longer description does not make unrelated changes coherent.

## Default Shape

Use this only when the repository has no template:

```markdown
## Context

Explain the existing problem, who or what it affects, and the decision behind the change. Make the paragraph understandable without the authoring session or linked discussion.

## Changes

- State each reviewer-visible outcome or behavior change.
- Name an important boundary or intentionally unchanged behavior when useful.
```

Use one short paragraph for context and one bullet per meaningful outcome. Do not force a minimum bullet count. Omit file inventories and implementation details that the diff communicates more clearly.

## Conditional Sections

| Section | Add when |
| --- | --- |
| `## Review notes` | The reviewer should focus on a tradeoff, uncertainty, generated file, or non-obvious part of the diff. State the feedback wanted. |
| `## User impact` | Behavior, UI, accessibility, documentation, or release communication changes for users. |
| `## Migration` | Compatibility breaks or adopters must take action. State what changes and how to adapt. |
| `## Rollout and rollback` | Deployment order, feature flags, data changes, or operational recovery affect risk. |
| `## Performance` | Measurements justify the approach or the change alters a performance budget. Give comparable numbers and conditions. |
| `## Screenshots` | A visual change is hard to judge from code. Prefer before and after views when both matter. |
| `## Validation` | Manual results cover behavior CI cannot prove, or CI is absent, failing, or intentionally skipped. |

Omit optional sections with no useful content. Put issue references and design links next to the claim they support unless a repository template requires a dedicated section.

## Validation

GitHub Checks or the repository's equivalent is the live record for automated tests. Do not copy CI job names, matrices, successful logs, or a status snapshot into the body.

Add a visible `Validation` section only when reviewers need information outside that live record:

- a manual UI, device, migration, compatibility, or accessibility check;
- a benchmark or experiment whose result informs the decision;
- missing, failing, flaky, or deliberately skipped CI;
- a short reproduction step the reviewer is expected to run.

Keep reviewer-useful reproduction steps visible. Put long command inventories, diagnostic output, or supporting logs in a `<details>` block. Omit successful command output. If nothing relevant ran and the repository expects this field, write `Not run:` with the reason.

## Writing Rules

- Use concise, plain English and define project-specific shorthand on first use.
- Do not refer to the current chat, earlier private discussion, or an unnamed request. Avoid phrases such as `as discussed` and `follow-up` without context.
- Explain decisions the code cannot show. Do not narrate how the author worked.
- Link issues and design documents, but keep the body understandable if a link becomes unavailable or the reader lacks access.
- State limitations or deliberate non-goals when they affect review or future maintenance.
- Recheck the body after the branch changes during review.

## Pattern Basis

This fallback distills recurring guidance from Google's [CL description](https://google.github.io/eng-practices/review/developer/cl-descriptions.html) and [small CL](https://google.github.io/eng-practices/review/developer/small-cls.html) guides, GitHub's [PR writing guidance](https://github.blog/developer-skills/github/how-to-write-the-perfect-pull-request/), Microsoft's [author guidance](https://microsoft.github.io/code-with-engineering-playbook/code-reviews/process-guidance/author-guidance/), and public templates from [React](https://github.com/react/react/blob/main/.github/PULL_REQUEST_TEMPLATE.md), [Kubernetes](https://github.com/kubernetes/kubernetes/blob/master/.github/PULL_REQUEST_TEMPLATE.md), [Next.js](https://github.com/vercel/next.js/blob/canary/.github/pull_request_template.md), [Grafana](https://github.com/grafana/grafana/blob/main/.github/PULL_REQUEST_TEMPLATE.md), and [Terraform](https://github.com/hashicorp/terraform/blob/main/.github/pull_request_template.md).
