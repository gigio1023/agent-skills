# Engineering Documentation Delivery Checklist

Apply this checklist to the changed scope, not mechanically to every page.

## Reader and Meaning

- [ ] The intended reader and primary job are clear.
- [ ] Required facts, actions, conditions, exceptions, uncertainty, and safety
      constraints remain intact.
- [ ] A style edit did not silently resolve a factual conflict.
- [ ] The page shape matches its job: task, reference, explanation, decision,
      onboarding, or contribution.

## Evidence and Accuracy

- [ ] Changed paths, links, anchors, commands, identifiers, defaults, units,
      environment variables, and version constraints match repository evidence.
- [ ] Examples use fake values and are labeled when they were not executed.
- [ ] Troubleshooting and failure behavior come from inspectable evidence.
- [ ] Contradictory or unavailable facts are surfaced rather than guessed.

## Structure and Navigation

- [ ] Sentences expose their main assertion without losing qualifiers.
- [ ] Bullets are parallel and nesting represents real hierarchy.
- [ ] Section openings lead with the action, lookup target, or decision.
- [ ] The page serves one primary job; supporting context still helps that job.
- [ ] Volatile duplicated facts have a maintained owner or a reason to remain.
- [ ] Inbound references were checked before headings or anchors changed.
- [ ] New Markdown or MDX syntax is supported by the target renderer.

## Scope and Delivery

- [ ] The diff contains no unrelated wording churn or implementation change.
- [ ] Repository documentation checks were run when available and proportionate.
- [ ] Executed, inspected-only, skipped, and unavailable checks are distinguished.
- [ ] Remaining uncertainty and the next minimal action are reported when they
      affect the reader's ability to rely on the document.
