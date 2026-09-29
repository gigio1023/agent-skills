# Functions and Modules

Read this when creating a module, writing a function whose task has more than one phase, deciding whether a block or a file should be split, moving code between modules, or changing public imports. The failure it exists to prevent has two faces: one function that carries a whole task because nothing named its pieces, and a pile of numbered helpers that were cut by line count. Both come from deciding the cut by size instead of by intent.

## Contents

- Name the pieces first
- When a block becomes a function
- Intent tests
- Flatten before splitting
- Effects at the edges
- Where code lives
- Sizes: review prompts and gates
- Ruff configuration for a new project
- Preserve behavior while moving code
- What a finished function meets
- Sources

## Name the pieces first

When creating a module, or a function whose task has more than one phase, write the skeleton before any body: a module docstring stating what the module owns and hides, then each function and class as an annotated signature with a one-sentence docstring and `...` as the body. Each docstring says what the function decides or produces for its caller. If a sentence needs "and" to join unrelated work, or the only honest name is a position such as `step_two`, `_part`, `process_data`, or `helper`, re-cut before writing any body. When a piece's intent is unclear, state the assumption in its docstring instead of absorbing the uncertainty into a longer body. Fill bodies once the skeleton reads as a complete account of the flow.

The skeleton is the module's table of contents, written before any body. For "report customers charged twice for the same invoice in a payments export", the failure is one `main()` that opens the file, parses rows, groups them, and prints, growing a section comment every twenty lines. The skeleton for the same task:

```python
"""Report customers charged twice for the same invoice in a payments export."""


class Charge(BaseModel):
    charge_id: str
    customer_id: str
    invoice_id: str
    amount: Decimal


def read_charges(path: Path) -> list[Charge]:
    """Parse the export; a row with a malformed amount is rejected, not skipped."""
    ...


def find_duplicates(charges: list[Charge]) -> dict[tuple[str, str], list[Charge]]:
    """Group by (customer, invoice) and keep the groups with more than one charge."""
    ...


def write_report(duplicates: dict[tuple[str, str], list[Charge]], out: TextIO) -> None:
    """One line per duplicate group, sorted by customer then invoice."""
    ...


def main(path: Path) -> int:
    """Exit 1 when duplicates exist, so a scheduler can alert on the exit code."""
    ...
```

Reading the skeleton already answers what the module does, which values flow between the phases, where the I/O is, and which decisions are pure. Each docstring is a small test of the cut: `read_charges` had to decide what happens to a bad row, and that decision is now visible before a line of parsing exists. Bodies are filled afterwards, each within its own signature; a body that wants to reach outside its signature is the sign that the skeleton needs another function, not that the body should grow.

Decomposition-first generation is the one technique with measured support: studies that generate function descriptions before implementations (Parsel, FunCoder, CodeChain, self-planning) report higher correctness, and self-planning also reports higher rated readability. The structural benefit is an inference from those results and from Ousterhout's "write the comments first"; no study has measured skeleton-first instructions against function length in a production agent.

## When a block becomes a function

Extract a block when a reader would otherwise have to work out what it does, and it hands back one named value, a decision, or a single effect through a small signature. Call count decides nothing in either direction: a responsibility called once still earns a function when its name states intent and its signature hides mechanism, and a helper with two callers is still wrong when its name says nothing more than its body. The measured SDKs show both sides: the Anthropic SDK extracts a single-caller `_attempt_request` because that step has its own contract, and its house style inlines a helper whose only justification is being called once. Vendor prompting guidance that says a "one-time operation" needs no helper means a statement or two, not a named step of the algorithm; read literally, it produces the giant function.

Keep a block inline when extracting it would need more than about four inputs, would return several unrelated locals, or would leave either function unreadable without the other. That is Fowler's own warning that extraction with many parameters and temporaries leaves code "scarcely more readable than the original", and Ousterhout's conjoined-methods red flag. When several state changes must happen in a strict order, keep them as one visible sequence with a comment at each ordering decision naming the failure it prevents; the longest functions that survive review in the measured libraries have exactly that shape, a resource lifetime whose order matters.

A comment that explains what a block does is a prompt to extract or rename. A comment that explains why stays.

## Intent tests

Each test tells a function that exists because of a responsibility from one that exists because a line count was hit. The agent applies them in its own review pass; a reviewer can apply them without running anything.

| Test | Passes when | Fails on |
| --- | --- | --- |
| Name | The name states what the function decides or produces: a noun phrase for a value, verb plus object for an effect, `is_` or `has_` for a predicate | `step_two`, `_process_part`, `handle_rest`, `do_validation_and_save` |
| One sentence | The docstring's first sentence is complete and joins no unrelated actions with "and" | "Validate the input and write the report" |
| Reason to change | One kind of change request would edit this function and none of its siblings | A function edited by every change |
| Signature | The parameters are what the function decides with; the return is one named value or model, not a tuple of the caller's locals; no flag argument selects between two behaviors | `_finish(a, b, c, d, e, mode=True) -> tuple[...]` |
| Caller | A reader of the caller, given only callee names, signatures, and docstrings, can state what the caller does, including every side effect | A callee named like a pure predicate that mutates shared state |
| Independence | The callee's body can be understood without the caller's loop state or ordering assumptions | A helper that only works because the caller ran a previous helper |
| Inline | Inlining the function back would not make the caller harder to read; if the body reads the same as the name, inline it | `def _clear_amount_owed(self): self.amount_owed = 0` |

## Flatten before splitting

Return early for invalid or trivial cases. Replace an `if`/`elif` chain over constant values with a mapping or a `match` before deciding that a function is too large; pydantic maps fifty types to handlers in a class-level dict with one method per case, and structlog picks one of six closures at construction time so the per-call method is one line. Cognitive complexity charges nesting and treats early returns as free, so a flat dispatch with guard clauses scores as the readable shape it is.

## Effects at the edges

Keep parsing or validation, computation, and output as separate phases joined by a Pydantic model or another named value; do not pass a tuple of locals between phases. I/O, network calls, persistence, and mutation of shared state belong in the function that orchestrates the phases; the computation beneath it stays pure. A function that mutates its arguments or other state says so in its name or docstring. Sync and async variants, or any other I/O variants, are thin wrappers around one pure core: the Anthropic SDK walks request parameters once in a pure function and defers file reads to a six-line sync and a six-line async entry point, while its sibling SDK still carries two 64-line walks that differ only by `await`.

## Where code lives

- **Helper placement.** A helper is a module-level function with a leading underscore, directly below its only caller; nest a function only to close over a local value, because Ruff's complexity rule adds a nested function's decisions to its parent and Google's guide forbids nesting merely to hide a name. Order a file by importance: the names a reader came for at the top.
- **Private by file, public by explicit re-export.** New modules start private (`_name.py`); the package's `__init__.py` re-exports the public surface deliberately through `__all__` or `from ._x import Name as Name`, the two forms type checkers recognize. A public module keeps the names, signatures, and docstrings callers import; its machinery lives in a private module beside it (pydantic's `fields.py` and `_internal/_fields.py`). `__all__` controls star imports; it is not access control.
- **Split by reason to change.** Split a module when its parts change for different reasons ("these change when the provider API changes, those when the report format changes"); keep together code that shares knowledge of one format, protocol, or invariant. Never split by kind (`all helpers`, `the first half`) or by line range. A module split out states why in its docstring: "Kept free of host-only imports so … can use it at module level", "Extracted so the poller, the runner, and the heartbeat all compute backoff the same way", "factored out to avoid import loops".
- **Leaf modules for shared vocabulary.** Exceptions, constants, and small shared types live in modules that import nothing from the package. Import a heavy central class lazily, or under `TYPE_CHECKING`, where the dependency would otherwise point upward; do not use either to hide a real dependency, and remember that Pydantic and documentation generators read annotations at runtime. Several files whose functions depend on each other in both directions are one module split badly, and a cycle closed through the package root works only until someone uses the name at import time.
- **Catch-all names.** `utils.py`, `common.py`, and a project-wide `models.py` are review signals: utility modules in well-run libraries stay small and narrow. They are not reasons to rename a cohesive existing module.

## Sizes: review prompts and gates

Numbers are backstops after writing, not targets while writing. Fowler declines to give "precise criteria", Ousterhout gives red flags without numbers, and Google sets "no hard limit". The evidence for keeping functions small at all is modest and one-directional: a study of 785K Java methods found lower later maintenance effort below about 24 lines, which supports smaller than typical, not tiny.

| Signal | Value | Role | Basis |
| --- | --- | --- | --- |
| Function body | about 40 lines | Review prompt: apply the intent tests | Google's guide; the measured libraries sit at a median of 2 to 7 body lines and a p90 of 16 to 37, with 50 lines at roughly the 95th to 98th percentile |
| Nesting | past 3 levels | Review prompt: flatten first | Cognitive complexity charges each level; depth 4 or more is 0.6% to 2.8% of functions in the measured libraries |
| Cyclomatic complexity (Ruff C901) | 10 | Gate in a new project | McCabe's limit; NIST SP 500-235 says limits up to 15 "have been used successfully" |
| Statements (PLR0915) | 50 | Gate in a new project | Formatter-stable, unlike line counts; a gate near 20 or 30 invites numbered splits |
| Arguments (PLR0913, PLR0917) | 7 total, 5 positional; off in tests | Gate in a new project | The default of 5 is the most-ignored size rule in sampled projects; pytest fixtures arrive as parameters; past a handful, parameters go keyword-only |
| Cognitive complexity | 15 | Optional gate through complexipy | Sonar's S3776 default; Ruff has no cognitive-complexity rule (issue #2418 is open) |
| Module | 500 lines review, 1,000 split or explain | Review prompt, first-party handwritten code | This pack's choice; Pylint and Sonar default to 1,000; Ruff declined a module-length rule twice because formatting changes line counts |

At the module prompts, judge cohesion and unit count, not length: the measured libraries keep files of 1,000 to 3,900 lines whose functions stay at 12 to 19 code lines each, and the largest function holds a median 6% to 13% of its file. A 2,000-line module of seventy named methods around one concept is acceptable; a 600-line module that is one function is not. Generated files, vendored code, migrations, declarative tables, and cohesive test matrices need contextual review, not extraction. Repository limits win over these values, and an existing repository keeps its configured thresholds; do not ratchet a threshold down as a side effect of an unrelated change.

## Ruff configuration for a new project

For a project this skill sets up. Only stable rules; PLR0904, PLR0914, and PLR1702 need preview mode, PLR0912 overlaps C901, and PLR0911 penalizes guard clauses. Selecting the rule matters: a `max-complexity` setting without `C901` in the selection has no effect.

```toml
[tool.ruff.lint]
extend-select = [
    "C901",     # cyclomatic complexity per function
    "PLR0913",  # too many arguments (self, cls, *args not counted)
    "PLR0915",  # too many statements: formatter-stable length backstop
    "PLR0917",  # too many positional arguments
]

[tool.ruff.lint.mccabe]
max-complexity = 10

[tool.ruff.lint.pylint]
max-args = 7
max-positional-args = 5
max-statements = 50

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["PLR0913", "PLR0917"]  # pytest fixtures arrive as parameters
```

Mature projects split on these rules: Litestar, pipx, and narwhals run near the defaults; pip and Home Assistant raise the complexity threshold to their current worst function; pytest, pandas, sphinx, and Warehouse turn the size rules off, Warehouse noting that adding C901 "would require refactoring". Size gates are hard to retrofit, which is why they belong at project start. None of the nine libraries measured for this skill relies on them; they control size with strict type checking, small units, and review, so a passing linter is a floor, not a design.

## Preserve behavior while moving code

1. Identify callers and the public surface: documented imports, package re-exports, entry points, type stubs, serialization names, and tests. Record the behavior to preserve using existing tests, or by running the caller-facing entry point on fixed input before and after the move.
2. Move the smallest cohesive responsibility and update its internal consumers. Keep an existing public import working through an intentional re-export or compatibility facade unless the user requested its removal; keep `__init__.py` imports intentional so a facade does not add expensive initialization, cycles, or hidden registration effects.
3. Check affected imports and configured dependency rules, then run focused tests and the repository's applicable static checks. Broaden when the moved code is shared, imported for side effects, or otherwise affects a wider surface.

Do not introduce a new runtime import cycle to complete an extraction. If the proposed split adds forwarding layers, forces tests to mock more internals, or makes routine changes touch more files, retain or revise the boundary; a file-length target does not justify that cost, and a shorter file is not a successful refactor if understanding it requires more cross-file navigation. Use existing import-linter or architecture checks when configured; adding one is in scope only when the change establishes the architecture, as [architecture selection](architecture-selection.md) describes.

## What a finished function meets

A finished function passes the intent tests and the configured Ruff rules. A complexity or statement-count finding identifies a function to re-cut by the rules above; do not answer it by moving line ranges into numbered helpers, and do not add `noqa` without a reason on the same line. The lint gate is the deterministic half of this contract: in a study of 1,650 Claude Code sessions, the odds of following a configured convention fell about 5.6% for each additional function generated, and the harness documentation calls instruction files advisory and hooks deterministic.

## Sources

Checked 2026-09-29. Measured figures are in [reference repositories](reference-repositories.md).

- Google, [Python Style Guide](https://google.github.io/styleguide/pyguide.html) sections 2.6 (nested functions), 2.7 (comprehensions), 3.18 (function length: "If a function exceeds about 40 lines, think about whether it can be broken up").
- [PEP 8](https://peps.python.org/pep-0008/) and [PEP 20](https://peps.python.org/pep-0020/): internal-name convention; "Flat is better than nested"; "If the implementation is hard to explain, it's a bad idea."
- Ruff [settings](https://docs.astral.sh/ruff/settings/), [C901](https://docs.astral.sh/ruff/rules/complex-structure/), [PLR0913](https://docs.astral.sh/ruff/rules/too-many-arguments/), [PLR0915](https://docs.astral.sh/ruff/rules/too-many-statements/), [PLR0917](https://docs.astral.sh/ruff/rules/too-many-positional-arguments/), [preview](https://docs.astral.sh/ruff/preview/); cognitive complexity [issue #2418](https://github.com/astral-sh/ruff/issues/2418); module length declined in [#10262](https://github.com/astral-sh/ruff/pull/10262) and [#21853](https://github.com/astral-sh/ruff/pull/21853).
- NIST, [SP 500-235](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication500-235.pdf) (1996) on the McCabe limit; SonarSource, [Cognitive Complexity](https://www.sonarsource.com/docs/CognitiveComplexity.pdf) v1.7 (2023); [complexipy](https://github.com/rohaquinlop/complexipy).
- Martin Fowler, [Function Length](https://martinfowler.com/bliki/FunctionLength.html) (2016) and [Extract Function](https://refactoring.com/catalog/extractFunction.html); Fowler and Beck, *Refactoring* 2nd ed., chapter 3 (Long Function, Divergent Change, Lazy Element, Mutable Data, Long Parameter List).
- John Ousterhout, *A Philosophy of Software Design* 2nd ed. (2021): deep modules, information hiding, "better together or better apart", the red flags, "write the comments first"; Ousterhout and Martin, [A Philosophy of Software Design vs Clean Code](https://github.com/johnousterhout/aposd-vs-clean-code) (2025).
- Robert C. Martin, [The Single Responsibility Principle](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html) (2014); John Carmack, [on inlined code](http://number-none.com/blow/john_carmack_on_inlined_code.html) (2007, preface 2014): "The real enemy addressed by inlining is unexpected dependency and mutation of state."
- Jack Diederich, [Stop Writing Classes](https://us.pycon.org/2012/schedule/presentation/352/) (PyCon 2012); Brandon Rhodes, [Hoist Your I/O](https://rhodesmill.org/brandon/slides/2015-05-pywaw/hoist/) (2015); Kent Beck, *Tidy First?* (2023), Extract Helper and its inverse One Pile.
- Chowdhury, Uddin, Holmes, [method size and maintenance effort](https://arxiv.org/abs/2205.01842) (MSR 2022); Muñoz Barón, Wyrich, Wagner, [cognitive complexity meta-analysis](https://arxiv.org/abs/2007.12520) (ESEM 2020).
- Decomposition-first generation: [Parsel](https://arxiv.org/abs/2212.10561), [FunCoder](https://arxiv.org/abs/2405.20092), [CodeChain](https://arxiv.org/abs/2310.08992), [self-planning](https://arxiv.org/abs/2303.06689). Kang, Seo, Kim ([EMNLP Findings 2024](https://arxiv.org/abs/2407.11406)) find decomposed output is not by itself more often correct; the process helps, the shape alone does not.
- LLM code shape: [AI-Generated Smells](https://arxiv.org/abs/2605.02741) (2026): Long Method where human baselines show none, and multi-file agent output split "without semantic cohesion"; [He et al.](https://arxiv.org/abs/2511.04427) (MSR 2026): codebase cognitive complexity rose after agent adoption under one estimator and not under another; [instruction adherence](https://arxiv.org/abs/2605.10039) (2026): compliance decays per generated function.
- Vendor guidance: [Claude Code best practices](https://code.claude.com/docs/en/best-practices) ("Unlike CLAUDE.md instructions which are advisory, hooks are deterministic"); [Claude prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) and [Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5) on one-time helpers; OpenAI [GPT-5 prompting guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide) ("Favor small, focused components").

The numbers in this file (about four inputs, 40 lines, the gate values, 500 and 1,000 lines) are this pack's choices anchored on the defaults above; only the C901 value rests on published evidence. Helper placement below the caller and the Pydantic model as the phase boundary are house preferences.
