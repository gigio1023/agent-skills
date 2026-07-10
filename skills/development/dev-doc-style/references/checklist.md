# Documentation Style Validation

Apply this checklist to changed content, not mechanically to every page in the
repository.

## Meaning

- [ ] The primary reader job is easier to identify or complete.
- [ ] Technical facts, conditions, exceptions, requirements, uncertainty, and
      citations retain their original meaning.
- [ ] No style judgment silently resolves a factual conflict.
- [ ] Examples and commands remain accurate or are explicitly unverified.

## Structure

- [ ] Sentences expose their main assertion.
- [ ] Bullets are parallel and nesting represents real hierarchy.
- [ ] Section openings provide useful context instead of meta narration.
- [ ] The page has one primary job; supporting material still serves it.
- [ ] Volatile duplicated facts have a clear owner where practical.

## Navigation and Rendering

- [ ] Changed local links and anchors resolve.
- [ ] Inbound links were checked before headings or sections were removed.
- [ ] New callouts, tabs, diagrams, or disclosure blocks match the target
      renderer.
- [ ] Descriptive links replace ambiguous "here" links where clarity improves.

## Scope

- [ ] The diff contains no unrelated rewrite or automatic site-wide convention.
- [ ] File splits and cross-page moves preserve discoverability and required
      standalone context.
- [ ] Repository documentation checks were run when available and proportionate;
      skipped checks are reported.

## Useful Checks

Adapt these to the repository and changed files:

```bash
rg -n 'old-heading|old-anchor' .
git diff --check
```

Use the repository's own Markdown linter, link checker, or docs build when it
exists. Do not claim a render or link check from visual inspection alone.
