# Python Architecture

Read this with [architecture selection](../architecture-selection.md) when the project is Python: it gives the Python spelling of the layouts, ports, composition root, domain models, agent-loop shape, and dependency-direction contracts. The decisions themselves (structure follows boundaries, abstractions follow triggers, the stop rules) live in the language-agnostic reference.

## Contents

- Layouts
- Ports as Protocols
- Wiring and lifetimes
- Domain models
- Agent loop in Python
- import-linter contracts
- Measurements
- Sources

## Layouts

Script, run with `uv run`:

```text
find_duplicate_charges.py   # PEP 723 header, models, pure functions, I/O functions, main()
```

CLI tool. `uv init --package` gives the `src/` layout; `uv init --no-package` suits a tool that nothing imports as a distribution.

```text
src/tool/
  __main__.py       # python -m tool
  cli.py            # argument parsing, exit codes, output formatting
  config/
    __init__.py     # re-exports Settings and load_settings
    _model.py       # Settings(BaseModel)
    _load.py        # reading files and environment
  sync/             # one package per capability, importable without argument parsing
    __init__.py
    _plan.py        # pure: decide what to copy
    _transfer.py    # I/O: perform the copy
  backends/         # only when a capability has several implementations: a Protocol plus a dict registry
```

CRUD service, framework-native and by feature:

```text
app/main.py  app/database.py  app/config.py
app/invoices/router.py  schemas.py  models.py  service.py
app/customers/router.py  schemas.py  models.py  service.py
```

Application with domain rules and several integrations:

```text
src/app/
  main.py                 # composition root: settings, adapters, services
  config.py               # settings model
  billing/
    __init__.py           # public surface of the feature
    model/
      _invoice.py         # Invoice entity and its state rules; no I/O imports
      _money.py           # frozen value objects
    service.py            # use cases: load, apply rules, call ports, save
    ports.py              # Protocols the use cases need, only for real seams
    api.py                # entry adapter for this feature, when it has one
  adapters/
    sqlite_store.py       # implements billing.ports.InvoiceStore
    stripe_gateway.py     # implements billing.ports.PaymentGateway
```

Pipeline or experiment code:

```text
src/pipeline/config.py  data/ (I/O)  features/ (pure)  model/ (no I/O)  train.py  evaluate.py
configs/train_small.toml    notebooks/   # import from src, never the reverse
```

Queue worker:

```text
src/worker/main.py  config.py  loop.py (receive, dispatch, acknowledge, retry)  handlers.py  policy.py (pure decisions)  ports.py  adapters/
```

## Ports as Protocols

A port is a `typing.Protocol` in the consuming feature's `ports.py`, declaring only the methods the caller uses. Adapters live in `adapters/` and do not subclass the port; the type checker checks conformance at the assignment site, and a controlled adapter satisfies the Protocol structurally. Use an ABC only when the base class carries behavior every implementation inherits or when a plugin system instantiates classes it discovered at runtime. Cosmic Python's authors, who use ABCs "for didactic reasons", report deleting them from production because Python "makes it too easy to ignore them".

```python
# src/app/billing/ports.py
class InvoiceStore(Protocol):
    def get(self, invoice_id: str) -> Invoice | None: ...
    def save(self, invoice: Invoice) -> None: ...


class PaymentGateway(Protocol):
    def charge(self, customer_id: str, amount: Decimal, reference: str) -> str:
        """Charge the customer and return the provider's charge id."""
        ...


# src/app/billing/service.py
class BillingService:
    def __init__(self, store: InvoiceStore, payments: PaymentGateway) -> None:
        self._store: InvoiceStore = store
        self._payments: PaymentGateway = payments

    def issue_and_charge(self, invoice_id: str) -> str:
        invoice: Invoice | None = self._store.get(invoice_id)
        if invoice is None:
            raise InvoiceError(f"unknown invoice {invoice_id}")
        invoice.issue()
        charge_id: str = self._payments.charge(invoice.customer_id, invoice.total(), invoice.invoice_id)
        invoice.mark_paid()
        self._store.save(invoice)
        return charge_id


# src/app/main.py, the only module that names concrete adapters
def build_billing(connection: sqlite3.Connection) -> BillingService:
    store: SqliteInvoiceStore = SqliteInvoiceStore(connection)
    payments: StripeGateway = StripeGateway(settings.stripe_key)
    return BillingService(store=store, payments=payments)
```

This sample project, with mypy `--strict` and the contracts below, was run on 2026-09-29.

## Wiring and lifetimes

The composition root (`main.py`, `create_app(settings)`, or `bootstrap()`) opens and closes connections through context managers or the framework's lifespan. Web frameworks already provide the per-request part (FastAPI `Depends` generators, Pyramid services); use it at the HTTP edge only and pass the session into the service layer. A DI container or service locator (dishka, dependency-injector, svcs) is justified by scoped dependency chains across many handlers, not by the number of classes; the dependency-injector documentation itself says its advantages "are not too important if you use Python as a scripting language".

## Domain models

Domain entities and value objects are `BaseModel`s: `frozen=True` for value objects, which then compare and hash by value, and methods for state changes and invariants. Pydantic performs no I/O, so a `BaseModel` domain runs and is checked without a database or network. SQLAlchemy's classical mapping onto a `BaseModel` fails at `session.add()`, so in a domain-rule feature the persistence adapter translates rows with `model_validate` or stores the model's JSON. In the library or SDK case, and on a measured hot path, the same records are dataclasses, `NamedTuple`, or plain classes so that users do not inherit Pydantic; the split and its consequences for validation are in [Pydantic integration](pydantic-integration.md).

## Agent loop in Python

The contract types are Pydantic models and `StrEnum`s; tool ports are Protocols; the budget decision is a pure function the loop calls before every step.

```python
class StopReason(StrEnum):
    COMPLETED = "completed"
    TURN_LIMIT = "turn_limit"
    TOKEN_LIMIT = "token_limit"
    DEADLINE = "deadline"


class Budget(BaseModel, frozen=True):
    max_turns: int
    max_tokens: int
    deadline_seconds: float


class LoopState(BaseModel, frozen=True):
    turns: int
    tokens: int
    elapsed_seconds: float
    task_done: bool


def next_stop(state: LoopState, budget: Budget) -> StopReason | None:
    """Return why the episode must stop now, or None to continue."""
    if state.task_done:
        return StopReason.COMPLETED
    if state.turns >= budget.max_turns:
        return StopReason.TURN_LIMIT
    if state.tokens >= budget.max_tokens:
        return StopReason.TOKEN_LIMIT
    if state.elapsed_seconds >= budget.deadline_seconds:
        return StopReason.DEADLINE
    return None


class SearchTool(Protocol):
    def search(self, query: str, limit: int) -> list[SearchHit]: ...
```

The production `SearchTool` adapter calls the retrieval service; a recorded adapter replays captured `SearchHit` lists keyed by query, so a real-run check or an evaluation episode is reproducible. The trajectory is a `BaseModel` with a list of step records and the final `StopReason`, written as JSON beside the end state.

## import-linter contracts

`include_external_packages = true` is required to forbid an external or standard-library module.

```toml
[tool.importlinter]
root_package = "app"
include_external_packages = true

[[tool.importlinter.contracts]]
name = "Billing rules stay free of I/O and of the use-case layer"
type = "forbidden"
source_modules = ["app.billing.model"]
forbidden_modules = ["sqlite3", "httpx", "app.billing.service", "app.billing.ports"]

[[tool.importlinter.contracts]]
name = "Composition root imports adapters; adapters import features; never the reverse"
type = "layers"
layers = ["app.main", "app.adapters", "app.billing"]

[[tool.importlinter.contracts]]
name = "Feature packages do not form import cycles"
type = "acyclic_siblings"
ancestors = ["app"]
depth = 0
```

Run it with the other checks, for example `uv run --group lint lint-imports`. Python tolerates package cycles as long as module-level cycles resolve, which is why feature packaging without a contract drifts toward an all-to-all graph.

## Measurements

The Pydantic domain sample was measured on Python 3.14.7 and Pydantic 2.13.5: 0.34 µs per frozen `BaseModel` construction against 0.18 µs for a frozen dataclass, which matters only for millions of objects in a hot loop.

## Sources

Accessed 2026-09-29.

- Hynek Schlawack, [Don't Mock What You Don't Own in 5 Minutes](https://hynek.me/articles/what-to-mock-in-5-mins/) (2022), [Subclassing in Python Redux](https://hynek.me/articles/python-subclassing-redux/) (2021); [svcs](https://svcs.hynek.me/en/stable/why.html) 26.2, [dishka](https://dishka.readthedocs.io/en/stable/) 1.10, [dependency-injector](https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html) 4.49 documentation.
- [import-linter](https://github.com/seddonym/import-linter/tree/main/docs) 2.15 contract types (`acyclic_siblings` since 2.6, `protected` since 2.5); [Python typing](https://docs.python.org/3/library/typing.html) on `Protocol` and `runtime_checkable`.
- Harry Percival and Bob Gregory, [Architecture Patterns with Python](https://www.cosmicpython.com/), on ABCs in production.

The agent-loop sample is this pack's illustration of the shape in the language-agnostic reference, not measured practice.
