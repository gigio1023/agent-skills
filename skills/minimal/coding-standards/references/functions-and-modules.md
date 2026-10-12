# Functions and Modules

Read this when creating a module, writing a function whose task has more than one phase, deciding whether a block or a file should be split, moving code between modules, or changing public imports. The failure it exists to prevent has two faces: one function that carries a whole task because nothing named its pieces, and a pile of numbered helpers that were cut by line count. Both come from deciding the cut by size instead of by intent. The Python spelling (a worked skeleton, private modules and re-exports, the Ruff gates, and the measured library numbers) is in [Python functions and modules](python/functions-and-modules.md).

## Contents

- Optional skeleton
- When a block becomes a function
- Intent tests
- Flatten before splitting
- Effects at the edges
- Where code lives
- Sizes: review prompts and gates
- Preserve behavior while moving code
- What a finished function meets
- Sources

## Optional skeleton

For a new module or multi-phase task with unclear boundaries, sketch a module responsibility, typed signatures, and short caller contracts before filling the bodies. A skeleton is a design aid, not a required intermediate artifact or a fixed generation order. Existing code may already expose the right responsibilities, and implementation may reveal a better boundary. Resolve consequential uncertainty before presenting it as a contract. Inspect vague names such as `step_two`, `_part`, `process_data`, or `helper` for a missing responsibility; a conjunction alone says nothing about cohesion.

Reading a skeleton reveals the values between phases, the I/O boundaries, and the pure decision. Each stated behavior, such as how malformed input is handled, must come from the task's requirements or an explicit design decision. If implementation requires hidden caller state or an awkward signature, revise the boundary or keep the cohesive sequence together. A worked Python skeleton is in the Python reference.

The studies cited below (Parsel, FunCoder, CodeChain, self-planning) motivated this design aid. They do not establish that every change needs a skeleton pass or that a particular function boundary is correct. The skill's rule is coherent responsibilities and readable data flow; skeleton-first generation is one way to reach it.

## When a block becomes a function

Extract a block when a reader would otherwise have to work out what it does, and it hands back one named value, a decision, or a single effect through a small signature. Call count decides nothing in either direction: a responsibility called once still earns a function when its name states intent and its signature hides mechanism, and a helper with two callers is still wrong when its name says nothing more than its body. The measured SDKs show both sides: the Anthropic SDK extracts a single-caller `_attempt_request` because that step has its own contract, and its house style inlines a helper whose only justification is being called once. Vendor prompting guidance that says a "one-time operation" needs no helper means a statement or two, not a named step of the algorithm; read literally, it produces the giant function.

Keep a block inline when extracting it would need more than about four inputs, would return several unrelated locals, or would leave either function unreadable without the other. That is Fowler's own warning that extraction with many parameters and temporaries leaves code "scarcely more readable than the original", and Ousterhout's conjoined-methods red flag. When several state changes must happen in a strict order, keep them as one visible sequence with a comment at each ordering decision naming the failure it prevents; the longest functions that survive review in the measured libraries have exactly that shape, a resource lifetime whose order matters.

A comment that explains what a block does is a prompt to extract or rename. A comment that explains why stays.

## Intent tests

Each test tells a function that exists because of a responsibility from one that exists because a line count was hit. The agent applies them in its own review pass; a reviewer can apply them without running anything.

| Test | Passes when | Fails on |
| --- | --- | --- |
| Name | The name states what the function decides or produces: a noun phrase for a value, verb plus object for an effect, `is_` or `has_` for a predicate | `step_two`, `_process_part`, `handle_rest` |
| Coherent contract | The summary names one responsibility and preserves its related actions, conditions, and side effects | A helper that combines independent validation and report-writing contracts without a meaningful shared responsibility |
| Reason to change | One kind of change request would edit this function and none of its siblings | A function edited by every change |
| Signature | The parameters are what the function decides with; the return is one named value or record, not a tuple of the caller's locals; no flag argument selects between two behaviors | `_finish(a, b, c, d, e, mode=True) -> tuple[...]` |
| Caller | A reader of the caller, given only callee names, signatures, and documentation, can state what the caller does, including every side effect | A callee named like a pure predicate that mutates shared state |
| Independence | The callee's body can be understood without the caller's loop state or ordering assumptions | A helper that only works because the caller ran a previous helper |
| Boundary value | The function makes its caller easier to read or isolates a meaningful contract; inline it when its name only repeats the body | `def _clear_amount_owed(self): self.amount_owed = 0` with no separate contract |

## Flatten before splitting

Return early for invalid or trivial cases. Replace a chain of conditionals over constant values with a lookup table or the language's pattern match before deciding that a function is too large. Cognitive complexity charges nesting and treats early returns as free, so a flat dispatch with guard clauses scores as the readable shape it is. A decision that does not change per call is made once at construction, so the per-call path stays short.

## Effects at the edges

Keep parsing or validation, computation, and output as separate phases joined by a named record type; do not pass a tuple of locals between phases. I/O, network calls, persistence, and mutation of shared state belong in the function that orchestrates the phases; the computation beneath it stays pure. A function that mutates its arguments or other state says so in its name or documentation. Sync and async variants, or any other I/O variants, are thin wrappers around one pure core rather than two copies of the logic that differ only by how they wait.

## Where code lives

- **Helper placement.** A private helper sits directly below its only caller; nest a function only to close over a local value, not merely to hide a name. Order a file by importance: the names a reader came for at the top.
- **Private by default, public by explicit export.** New modules start private, and the package exports its public surface deliberately. A public module keeps the names, signatures, and documentation callers import; its machinery lives in a private module beside it. Visibility conventions are not access control.
- **Split by reason to change.** Split a module when its parts change for different reasons ("these change when the provider API changes, those when the report format changes"); keep together code that shares knowledge of one format, protocol, or invariant. Never split by kind (`all helpers`, `the first half`) or by line range. A module split out states why in its header documentation: "Kept free of host-only imports so … can use it at module level", "Extracted so the poller, the runner, and the heartbeat all compute backoff the same way", "factored out to avoid import loops".
- **Leaf modules for shared vocabulary.** Errors, constants, and small shared types live in modules that import nothing from the package. Defer a heavy import where the dependency would otherwise point upward, but never to hide a real dependency. Several files whose functions depend on each other in both directions are one module split badly.
- **Catch-all names.** `utils`, `common`, and a project-wide `models` module are review signals: utility modules in well-run libraries stay small and narrow. They are not reasons to rename a cohesive existing module.

## Sizes: review prompts and gates

Function-size numbers are backstops after writing, not targets while writing. Fowler declines to give "precise criteria", Ousterhout gives red flags without numbers, and Google sets "no hard limit". The evidence for keeping functions small at all is modest and one-directional: a study of 785K Java methods found lower later maintenance effort below about 24 lines, which supports smaller than typical, not tiny.

| Signal | Value | Role | Basis |
| --- | --- | --- | --- |
| Function body | about 40 lines | Review prompt: apply the intent tests | Google's guide; the measured Python libraries sit at a median of 2 to 7 body lines |
| Nesting | past 3 levels | Review prompt: flatten first | Cognitive complexity charges each level |
| Cyclomatic complexity | 10 | Gate in a new project | McCabe's limit; NIST SP 500-235 says limits up to 15 "have been used successfully" |
| Statements per function | 50 | Gate in a new project | Formatter-stable, unlike line counts; a gate near 20 or 30 invites numbered splits |
| Arguments | 7 total, 5 positional; off in tests | Gate in a new project | Past a handful, parameters are passed by name |
| Cognitive complexity | 15 | Optional gate | Sonar's S3776 default |
| File | about 500 handwritten lines: split at a named boundary; past 1,000: only with a stated reason | Default for first-party handwritten code | This pack's choice: small files and deep directories |

Size prompts the split; cohesion picks the cut. A 600-line module that is one function fails on both counts, and splitting it by line range fixes neither. A file that stays above 1,000 lines is one cohesive unit, such as a parser, a protocol state machine, or a mirrored sync and async pair that cannot share more code, and the change summary says why. The measured Python libraries keep files of 1,000 to 3,900 lines of small units around one concept; that is library practice under import-cost and compatibility pressure, recorded as evidence, not this skill's target. Generated files, vendored code, migrations, declarative tables, and cohesive test matrices need contextual review, not extraction. Repository limits win over these values, and an existing repository keeps its configured thresholds; do not ratchet a threshold down as a side effect of an unrelated change. Size gates are hard to retrofit, which is why they belong at project start; a passing linter is a floor, not a design.

## Preserve behavior while moving code

1. Identify callers and the public surface: documented imports, package exports, entry points, type declarations, serialization names, and tests. Record the behavior to preserve using existing tests, or by running the caller-facing entry point on fixed input before and after the move.
2. Move the smallest cohesive responsibility and update its internal consumers. Keep an existing public import working through an intentional re-export or compatibility facade unless the user requested its removal; keep package entry modules free of expensive initialization, cycles, and hidden registration effects.
3. Check affected imports and configured dependency rules, then run the real entry point on the same fixed input and the repository's applicable checks. Broaden when the moved code is shared, imported for side effects, or otherwise affects a wider surface.

Do not introduce a new runtime import cycle to complete an extraction. If the proposed split adds forwarding layers, forces checks to fake more internals, or makes routine changes touch more files, retain or revise the boundary. A shorter file is not a successful refactor if understanding it requires more cross-file navigation than the boundary saves. Use existing dependency-rule checks when configured; adding one is in scope only when the change establishes the architecture, as [architecture selection](architecture-selection.md) describes.

## What a finished function meets

A finished function satisfies the caller's contract and the configured checks. Use the intent tests to review its responsibility and readability. A complexity or statement-count finding identifies a function to inspect; do not answer it by moving line ranges into numbered helpers, and do not add a suppression without a reason on the same line. A configured lint gate enforces its own measurable rule, not semantic cohesion or readability.

## Sources

Checked 2026-09-29. Measured figures and Python-specific sources are in [Python functions and modules](python/functions-and-modules.md) and [Python reference repositories](python/reference-repositories.md).

- Google, [Python Style Guide](https://google.github.io/styleguide/pyguide.html) section 3.18 (function length: "If a function exceeds about 40 lines, think about whether it can be broken up").
- NIST, [SP 500-235](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication500-235.pdf) (1996) on the McCabe limit; SonarSource, [Cognitive Complexity](https://www.sonarsource.com/docs/CognitiveComplexity.pdf) v1.7 (2023).
- Martin Fowler, [Function Length](https://martinfowler.com/bliki/FunctionLength.html) (2016) and [Extract Function](https://refactoring.com/catalog/extractFunction.html); Fowler and Beck, *Refactoring* 2nd ed., chapter 3 (Long Function, Divergent Change, Lazy Element, Mutable Data, Long Parameter List).
- John Ousterhout, *A Philosophy of Software Design* 2nd ed. (2021): deep modules, information hiding, "better together or better apart", the red flags, "write the comments first"; Ousterhout and Martin, [A Philosophy of Software Design vs Clean Code](https://github.com/johnousterhout/aposd-vs-clean-code) (2025).
- Robert C. Martin, [The Single Responsibility Principle](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html) (2014); John Carmack, [on inlined code](http://number-none.com/blow/john_carmack_on_inlined_code.html) (2007, preface 2014): "The real enemy addressed by inlining is unexpected dependency and mutation of state."
- Kent Beck, *Tidy First?* (2023), Extract Helper and its inverse One Pile.
- Chowdhury, Uddin, Holmes, [method size and maintenance effort](https://arxiv.org/abs/2205.01842) (MSR 2022); Muñoz Barón, Wyrich, Wagner, [cognitive complexity meta-analysis](https://arxiv.org/abs/2007.12520) (ESEM 2020).
- Decomposition-first generation: [Parsel](https://arxiv.org/abs/2212.10561), [FunCoder](https://arxiv.org/abs/2405.20092), [CodeChain](https://arxiv.org/abs/2310.08992), [self-planning](https://arxiv.org/abs/2303.06689). Kang, Seo, Kim ([EMNLP Findings 2024](https://arxiv.org/abs/2407.11406)) find decomposed output is not by itself more often correct; the process helps, the shape alone does not.
- LLM code shape: [AI-Generated Smells](https://arxiv.org/abs/2605.02741) (2026): Long Method where human baselines show none, and multi-file agent output split "without semantic cohesion"; [He et al.](https://arxiv.org/abs/2511.04427) (MSR 2026): codebase cognitive complexity rose after agent adoption under one estimator and not under another; [instruction adherence](https://arxiv.org/abs/2605.10039) (2026): compliance decays per generated function.
- Vendor guidance: [Claude Code best practices](https://code.claude.com/docs/en/best-practices) ("Unlike CLAUDE.md instructions which are advisory, hooks are deterministic"); [Claude prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) and [Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5) on one-time helpers; OpenAI [GPT-5 prompting guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide) ("Favor small, focused components").

The numbers in this file (about four inputs, 40 lines, the gate values, 500 and 1,000 lines) are this pack's choices anchored on the defaults above; only the cyclomatic value rests on published evidence. Helper placement below the caller and a named record as the phase boundary are house preferences.
