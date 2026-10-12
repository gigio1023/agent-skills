# Python Functions and Modules

Read this with [functions and modules](../functions-and-modules.md) when the code is Python: it holds a worked skeleton, Python's mechanics for private modules and re-exports, dispatch and I/O-variant examples from measured libraries, the Ruff gates a new project adopts, and the Python-specific steps of moving code. The intent tests, the size prompts, and the move procedure themselves are in the language-agnostic reference.

## Contents

- Worked skeleton
- Flattening in Python
- Sync and async variants
- Where code lives in Python
- Python size evidence
- Ruff configuration for a new project
- Moving Python code
- Sources

## Worked skeleton

For "report customers charged twice for the same invoice in a payments export", a skeleton can expose parsing, duplicate detection, and reporting before they accumulate inside one `main()`. One possible sketch:

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

Reading this skeleton reveals the values between phases, the I/O boundaries, and the pure decision. `read_charges` states how malformed input is handled; that choice must come from the task's requirements or an explicit design decision.

## Flattening in Python

Replace an `if`/`elif` chain over constant values with a mapping or a `match` before deciding that a function is too large. pydantic maps fifty types to handlers in a class-level dict with one method per case, and structlog picks one of six closures at construction time so the per-call method is one line.

## Sync and async variants

The Anthropic SDK walks request parameters once in a pure function and defers file reads to a six-line sync and a six-line async entry point, while its sibling SDK still carries two 64-line walks that differ only by `await`. Phases are joined by a Pydantic model where the project uses Pydantic, or by another named record.

## Where code lives in Python

- **Helper placement.** A helper is a module-level function with a leading underscore, directly below its only caller. Nest a function only to close over a local value, because Ruff's complexity rule adds a nested function's decisions to its parent and Google's guide forbids nesting merely to hide a name.
- **Private by file, public by explicit re-export.** New modules start private (`_name.py`); the package's `__init__.py` re-exports the public surface deliberately through `__all__` or `from ._x import Name as Name`, the two forms type checkers recognize. A public module keeps the names, signatures, and docstrings callers import; its machinery lives in a private module beside it (pydantic's `fields.py` and `_internal/_fields.py`). `__all__` controls star imports; it is not access control.
- **Leaf modules and deferred imports.** Exceptions, constants, and small shared types live in modules that import nothing from the package. Import a heavy central class lazily, or under `TYPE_CHECKING`, where the dependency would otherwise point upward; do not use either to hide a real dependency, and remember that Pydantic and documentation generators read annotations at runtime. A cycle closed through the package root works only until someone uses the name at import time.
- **Catch-all names.** `utils.py`, `common.py`, and a project-wide `models.py` are review signals.

## Python size evidence

| Signal | Python measurement | Rule it supports |
| --- | --- | --- |
| Function body | Median 2 to 7 body lines and p90 16 to 37 in the nine measured libraries; 50 lines sits at roughly the 95th to 98th percentile | About 40 lines as a review prompt |
| Nesting | Depth 4 or more is 0.6% to 2.8% of functions | Past 3 levels as a review prompt |
| Arguments | Ruff's default of 5 is the most-ignored size rule in sampled projects; pytest fixtures arrive as parameters | 7 total, 5 positional, off in tests; past a handful, keyword-only |
| Cognitive complexity | Ruff has no cognitive-complexity rule (issue #2418 is open); complexipy implements Sonar's | Optional gate at 15 |
| Module length | Pylint and Sonar default to 1,000 lines; Ruff declined a module-length rule twice because formatting changes line counts | This pack's 500 and 1,000 file prompts |

The measured libraries keep files of 1,000 to 3,900 lines whose functions stay at 12 to 19 code lines each, and the largest function holds a median 6% to 13% of its file. Evidence and commits are in [reference repositories](reference-repositories.md).

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

Mature projects split on these rules: Litestar, pipx, and narwhals run near the defaults; pip and Home Assistant raise the complexity threshold to their current worst function; pytest, pandas, sphinx, and Warehouse turn the size rules off, Warehouse noting that adding C901 "would require refactoring". None of the nine libraries measured for this skill relies on them; they control size with strict type checking, small units, and review. Do not add `noqa` without a reason on the same line.

## Moving Python code

The public surface includes documented imports, `__init__.py` re-exports, entry points in `pyproject.toml`, type stubs, and serialization names. Keep `__init__.py` imports intentional so a facade does not add expensive initialization, cycles, or hidden registration effects. Use existing import-linter contracts when configured; their setup is in [Python architecture](architecture.md).

## Sources

Checked 2026-09-29.

- Google, [Python Style Guide](https://google.github.io/styleguide/pyguide.html) sections 2.6 (nested functions), 2.7 (comprehensions), 3.18 (function length).
- [PEP 8](https://peps.python.org/pep-0008/) and [PEP 20](https://peps.python.org/pep-0020/): internal-name convention; "Flat is better than nested"; "If the implementation is hard to explain, it's a bad idea."
- Ruff [settings](https://docs.astral.sh/ruff/settings/), [C901](https://docs.astral.sh/ruff/rules/complex-structure/), [PLR0913](https://docs.astral.sh/ruff/rules/too-many-arguments/), [PLR0915](https://docs.astral.sh/ruff/rules/too-many-statements/), [PLR0917](https://docs.astral.sh/ruff/rules/too-many-positional-arguments/), [preview](https://docs.astral.sh/ruff/preview/); cognitive complexity [issue #2418](https://github.com/astral-sh/ruff/issues/2418); module length declined in [#10262](https://github.com/astral-sh/ruff/pull/10262) and [#21853](https://github.com/astral-sh/ruff/pull/21853); [complexipy](https://github.com/rohaquinlop/complexipy).
- Jack Diederich, [Stop Writing Classes](https://us.pycon.org/2012/schedule/presentation/352/) (PyCon 2012); Brandon Rhodes, [Hoist Your I/O](https://rhodesmill.org/brandon/slides/2015-05-pywaw/hoist/) (2015).

Only the C901 value rests on published evidence; the other gate values are this pack's choices anchored on the defaults above.
