# Python Documentation Review Checklist

Apply this checklist to the requested symbols and changed files.

## Surface Selection

- [ ] Public exports, re-exports, protocols, abstract methods, callbacks, and
      framework entry points were considered.
- [ ] Private helpers were documented only for a non-obvious invariant or
      external constraint.
- [ ] Generated, vendored, migration, and third-party files remain untouched
      unless explicitly in scope.

## Contract Accuracy

- [ ] Purpose describes effect or responsibility rather than repeating the name.
- [ ] Parameter text adds units, accepted forms, sentinel, ownership, mutation,
      or normalization semantics instead of duplicating annotations.
- [ ] Return or yield text covers ordering, laziness, ownership, mutability, and
      empty behavior when callers need them.
- [ ] Exceptions are intentionally exposed API behavior, not an exhaustive list
      of incidental lower-level failures.
- [ ] Side effects, partial success, cleanup, retry, caching, and fallback claims
      have implementation, test, spec, or user evidence.
- [ ] Async cancellation, generator timing, context-manager lifecycle, protocol
      obligations, and subclass behavior are covered when applicable.

## Style and Placement

- [ ] Repository configuration or generator requirements determined the format.
- [ ] Exact signature parameter names are used.
- [ ] Summary lines are useful to generated indexes.
- [ ] Nearby conflicts did not trigger an unrelated format conversion.
- [ ] Inline comments sit above the smallest relevant block and explain why,
      invariants, or external constraints.
- [ ] Tool directives remain unchanged unless their behavior was explicitly in
      scope.

## Scope and Verification

- [ ] Signatures, annotations, decorators, imports, control flow, and executable
      statements did not change during a doc-only request.
- [ ] Changed files parse or compile.
- [ ] Required repository checks and applicable docstring, lint, or docs-build
      checks ran; type or runtime tests were added only for a specific claim or
      tool-sensitive change, rather than every prose edit.
- [ ] The doc-only diff guard passed when a Git base was available.
- [ ] Each final claim was re-read against current code and tests.
- [ ] Skipped checks and unresolved intent are reported where material.

## Review Finding Shape

For each actionable finding, provide:

1. symbol and location;
2. false, missing, redundant, or speculative contract;
3. caller or maintenance impact;
4. supporting evidence;
5. smallest repair.

Do not inflate a review with trivial private functions or style preferences that
the repository does not enforce.
