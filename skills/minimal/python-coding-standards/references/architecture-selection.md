# Architecture Selection

Read this when starting a project, adding a package, introducing an interface, wiring an integration, or when asked which architecture a Python project should use. The shape is chosen from the project kind, then per feature inside the project, and it changes only when a named trigger has actually occurred. An agent that generates a hexagonal skeleton for a hundred-line tool and an agent that puts a payment system in one file are making the same mistake from opposite ends: neither read the row.

## Contents

- Choose the row
- Layouts
- Growth path
- Ports, adapters, and wiring
- Models in the domain
- Enforcing import direction
- Stop rules
- Pattern catalog and the authors' own limits
- Evidence
- Sources

## Choose the row

| Project kind | Shape | Import direction | Escalate when | Over-engineered when |
| --- | --- | --- | --- | --- |
| One-off script, notebook-adjacent code | One module: models, pure rules, I/O helpers, `main()`; PEP 723 header, run with `uv run` | None inside the file; a notebook imports the module, never the reverse | A second entry point, a second importer, a test that needs setup, or about 500 lines | Classes with one method, ABCs, a package, a configuration framework |
| CLI tool | Flat package: `cli.py`, one module per capability, `commands/` when subcommands multiply | `cli` imports capabilities; capabilities never import `cli` | A capability grows its own model, rules, and I/O; a second backend appears | Service classes wrapping functions, repositories for files, a DI container |
| Library or SDK | Public surface in `__init__.py` over private `_` modules; public models and exceptions | Public modules import private ones; no composition root inside the library | Optional integrations as extras plus an adapter module; sync and async variants | Application layers or a container imposed on callers |
| HTTP service with little domain logic | Framework-native: routes, ORM models, schemas, query functions; by kind while small, by feature when larger | routes to services or query functions to ORM models; no package cycles | A feature gains rules worth testing without the database; an integration gets a second implementation | A repository over the ORM session, pass-through service classes, DTO mappers between identical shapes |
| Application with real domain rules and several integrations | Feature packages: pure `model.py`, `service.py` use cases, `ports.py` Protocols for real seams, `adapters/`, one composition root | `main` to `adapters` to features; `model` imports no I/O and no `service` | Several features must stay independent (modular monolith); one event fans out to several handlers (message bus) | A port per class, a repository per entity, a unit of work over one repository, CQRS without a read problem |
| Data or ML pipeline, experiment code | Functional core (transforms, model definition) plus entry scripts as the shell; one configuration model | Entry scripts import the core; the core imports no storage, tracking, or CLI | Several storage backends; several entry points sharing stages | Repositories for datasets, a service layer around a training loop |
| Long-running worker or agent | Loop shell, handler functions, pure decision logic, Protocol ports for the model client, queue, and store | `main` to adapters to loop and handlers to core | Many message types with several handlers each; per-message scoped resources | A message bus with one event type, a plugin registry with one plugin |
| Large application, several teams | Modular monolith: top-level packages by business area, each with one public surface | Areas import each other only through their public module; no package cycles | Independent deployment or scaling becomes a measured need | Separate deployables or an in-process broker between areas |

Choose per feature, not per project: a CRUD feature stays flat beside a feature with ports. State the chosen row in the change summary when creating a project or a package, with the trigger that would move it to the next row.

## Layouts

Files exist when they have content. In the production applications inspected, `service.py` appears in most feature packages and `flows.py` or `tasks.py` only where a feature has flows or tasks; no feature carries an empty template.

Script:

```text
find_duplicate_charges.py   # PEP 723 header, models, pure functions, I/O functions, main()
```

CLI tool:

```text
src/tool/
  __main__.py     # python -m tool
  cli.py          # argument parsing, exit codes, output formatting
  sync.py         # one module per capability, importable without argument parsing
  config.py       # configuration model and loading
  backends/       # only when a capability has several implementations: a Protocol plus a dict registry
```

CRUD service, small (layered by kind) and larger (by feature):

```text
app/main.py  app/api/deps.py  app/api/routes/items.py  app/models.py  app/crud.py  app/core/

app/main.py  app/database.py  app/config.py
app/invoices/router.py  schemas.py  models.py  service.py
```

Application with domain rules and several integrations:

```text
src/app/
  main.py                 # composition root: settings, adapters, services
  config.py               # settings model
  billing/
    model.py              # entities, value objects, rules; no I/O imports
    service.py            # use cases: load, apply rules, call ports, save
    ports.py              # Protocols the use cases need, only for real seams
    api.py                # entry adapter for this feature, when it has one
  adapters/
    sqlite_store.py       # implements billing.ports.InvoiceStore
    stripe_gateway.py     # implements billing.ports.PaymentGateway
tests/test_billing.py     # in-memory fakes of the ports
```

Pipeline or experiment code:

```text
src/pipeline/config.py  data.py (I/O)  features.py (pure)  model.py (no I/O)  train.py  evaluate.py
configs/train_small.toml    notebooks/   # import from src, never the reverse
```

Worker or agent:

```text
src/agent/main.py  config.py  loop.py (receive, dispatch, acknowledge, retry)  handlers.py  policy.py (pure decisions)  ports.py  adapters/
```

Ports arrive earlier in a worker than in a CRUD service because deterministic tests need a fake model client and queue; faking a Protocol the code owns replaces mocking a vendor SDK.

## Growth path

Each step moves code and, where public imports exist, re-exports it; tests written against public functions keep passing. The move order itself is in [functions and modules](functions-and-modules.md).

| Stage | Shape | Trigger to enter | First move |
| --- | --- | --- | --- |
| 0 | One module | Start of any small tool | Rules in pure functions; I/O only in `main()` and named I/O helpers |
| 1 | Package split by responsibility | A second entry point, a second importer, a test needing setup, or about 500 lines | `uv init --package`; move the pure rules into a module with no I/O imports |
| 2 | Feature packages | Two or more features with separate vocabulary whose changes cluster separately | Group each feature's model, operations, and entry adapter; keep shared code small |
| 3 | An explicit port for one integration | A second implementation (vendor, environment, or null variant), or a test that would otherwise mock a third-party library | A Protocol in the consuming feature's `ports.py`, an adapter module, wiring in `main.py` |
| 4 | Enforced direction | A rule that people or agents have broken, or several features that must stay independent | import-linter `forbidden`, `layers`, `acyclic_siblings`, or `independence` contracts |
| 5 | Service layer, unit of work, message bus, container | The triggers the pattern catalog lists | One pattern at a time, where the pain is |

The first extraction is always the functional core: the rule that decides, pulled out of the code that reads and writes. Cosmic Python's first refactor is exactly this, a pure `determine_actions()` separated from the filesystem calls. The service layer's legitimate origin is a second entry point (HTTP plus worker, CLI plus API) that would otherwise duplicate orchestration; the book's own advice is to introduce it "after you spot orchestration logic creeping into your controllers".

## Ports, adapters, and wiring

A port is a `typing.Protocol` in the consuming feature's `ports.py`, declaring only the methods the caller uses. Adapters live in `adapters/` and do not subclass the port; conformance is checked by the type checker at the assignment site, and a test fake in the test module satisfies the Protocol structurally. Use an ABC only when the base class carries behavior every implementation inherits (then it is a base class, not only a port) or when a plugin system instantiates classes it discovered at runtime. Cosmic Python's authors, who use ABCs "for didactic reasons", report deleting them from production because Python "makes it too easy to ignore them".

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

Services receive collaborators through annotated constructor parameters and never construct clients themselves. One composition root (`main.py`, `create_app(settings)`, or `bootstrap()`) names the concrete adapters and owns their lifetimes, opening and closing connections through context managers or the framework's lifespan; tests call it with fakes or build services directly. Web frameworks already provide the per-request part (FastAPI `Depends` generators, Pyramid services); use it at the HTTP edge only and pass the session into the service layer. A DI container or service locator (dishka, dependency-injector, svcs) is justified by scoped dependency chains across many handlers, not by the number of classes; none of the production applications inspected uses one, and the dependency-injector documentation itself says its advantages "are not too important if you use Python as a scripting language". This sample project, with tests, mypy `--strict`, and the contracts below, was run on 2026-09-29.

## Models in the domain

Domain entities and value objects are `BaseModel`s: frozen for value objects, methods for state changes and invariants. The rule that protects the domain is "the model module imports no I/O", not "no third-party imports"; Pydantic performs no I/O, so a `BaseModel` domain runs and tests without a database or network. ORM classes are a framework-required representation: in a CRUD feature the ORM entity is the working object and services operate on it; in a domain-rule feature the persistence adapter translates rows to models, because SQLAlchemy's classical mapping onto a `BaseModel` fails at `session.add()`. Reuse the domain model as the API schema while exposure and naming match; a separate schema model appears when the public contract differs. In the library or SDK row, and on a measured hot path, the same records are dataclasses or plain classes so that users do not inherit Pydantic; the split and its consequences for validation are in [Pydantic integration](pydantic-integration.md).

## Enforcing import direction

Add import-linter contracts when the change establishes the architecture, that is, when the request creates the project or the package boundary; an ordinary change does not add a checker as a side effect. The first contract is the one that matters: the model module imports no I/O. `include_external_packages = true` is required to forbid an external or standard-library module.

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

Run it with the other checks, for example `uv run --group lint lint-imports`. Three of the four production applications inspected have package-level import cycles that `acyclic_siblings` would have reported (Dispatch would need 108 edges removed, Polar 296, Warehouse 31); none enforces direction. Python tolerates package cycles as long as module-level cycles resolve, so feature packaging without a contract drifts toward an all-to-all graph.

## Stop rules

The concrete failure: asked for a hundred-line tool that renames photos by capture date, an agent generates entity, value-object, repository-ABC, use-case-ABC plus `Impl`, infrastructure, presentation, and container modules with six `__init__.py` files. Reading one behavior then takes six files, renaming a field touches five, three interfaces have one implementation, and the tests mock the repository instead of checking renamed files.

1. **Match the row first.** Stay in the current row until a trigger from the table has actually occurred.
2. **No file without content.** No empty modules, placeholder packages, or a per-feature file template before something goes in them.
3. **No interface with one implementation**, except a Protocol at an I/O boundary whose fake a test in the same change uses. Never an interface for a use case, a service, or a model class.
4. **No repository over an ORM in a CRUD feature.** Call the session or query functions. A repository is for an aggregate whose rules are tested without the database, or for storage with two implementations.
5. **No forwarding service.** A use-case function loads, decides, causes a side effect, and saves, or it does not exist.
6. **No unit of work, message bus, domain events, or CQRS by default.** A unit of work when one use case must commit several repositories atomically and the ORM session is not enough; a bus when one event triggers several independent side effects; CQRS read models when reads are a measured problem.
7. **No DI container while the composition root fits on one screen.**
8. **Shape per feature.** A CRUD feature stays flat next to a feature with ports; the top level goes by feature once a layer package grows.
9. **Scaffolding never outweighs behavior.** No seedwork, base classes, or generic repositories before two features need the same code. Duplication is cheaper than the wrong abstraction.
10. **No restructuring as a side effect.** An existing repository keeps its shape unless the request is to change it. When a generated layout has more architecture files than files containing rules or integration code, collapse it to the previous row.

## Pattern catalog and the authors' own limits

| Pattern | Smallest Python expression | The authors' own precondition or warning |
| --- | --- | --- |
| Layered (presentation, domain, data) | Three modules or packages; lower ones never import higher ones | Fowler: "should only be applied at a relatively small granularity"; once a layer gets too big, "split your top level into domain oriented modules which are internally layered" |
| Ports and adapters (hexagonal) | Protocol ports in the consuming feature, adapter modules, one composition root | Cockburn: "favor a small number, two, three or four ports"; the pattern "says nothing about the structure of the inside of the hexagon" |
| Clean and onion | Identical to the ports sample; the rings are `model.py`, `service.py`, `adapters/`, `main.py` | Martin calls the circles "schematic"; Palermo: "not appropriate for small websites … appropriate for long-lived business applications" |
| DDD tactical patterns | Entity: `BaseModel` with an id and rule methods. Value object: frozen `BaseModel`. Aggregate: a root that owns its children, one changed per transaction. Domain service: a module-level function. Factory: a classmethod. Event: a frozen `BaseModel` on the aggregate's `events` list | Fowler: "particularly suited to complex domains"; Evans: "Make the core small"; Vernon: true invariants, small aggregates, reference by identity |
| Repository | A Protocol with `get` and `add` or `save`, a SQL adapter, an in-memory fake | Cosmic Python: "If your app is just a simple CRUD … wrapper around a database, then you don't need a domain model or a repository"; "An ORM already buys you some decoupling" |
| Service layer | Use-case functions taking primitives and dependencies | "If your app is purely a web app, your controllers/view functions can be the single place to capture all the use cases"; risk of the anemic domain model |
| Unit of work | A context manager exposing repositories and `commit()` | "You can go a long way just passing a session around" |
| Domain events and message bus | An events list on the aggregate; a dict from event type to handlers | "there is no single place in the system where you can understand how a request will be fulfilled"; synchronous handlers slow endpoints |
| CQRS | Read views as raw SQL functions | "Can't I just use repositories? Of course you can!" |
| Vertical slice, feature packages | One package per capability with its router, schemas, models, and service functions | Bogard: the team must "recognize when to push complex logic into the domain", else "this pattern is likely not for you" |
| Functional core, imperative shell | Pure functions or model methods that take values and return decisions; a thin shell that reads, calls, and applies | Bernhardt: the shell has "few conditionals"; works at any size |
| Modular monolith | Top-level business packages with one public module each, enforced by `independence` or `acyclic_siblings` | Grzybek: modules need "a well-defined interface/contract"; Fowler: find the boundaries by building the monolith first |

## Evidence

Inspected on 2026-09-29 from shallow clones.

| Repository | Size | Shape | Ports | Wiring | Package cycles |
| --- | --- | --- | --- | --- | --- |
| cosmicpython/code `14c84797` | 20 files, 736 lines | By layer: domain, service_layer, adapters, entrypoints | ABCs for repository, unit of work, notifications | `bootstrap()` with signature-based injection | None |
| Netflix/dispatch `dd2837e8` (archived 2025) | 493 files, 62,323 lines | 68 feature packages plus `plugins/` | 26 plugin base classes | FastAPI `Depends`; database-configured plugin lookup | 108 edges to remove |
| fastapi/full-stack-fastapi-template `cb740b65` | 19 files, 1,153 lines | By kind: api, core, crud, models | None | FastAPI `Depends` | 1 edge |
| polarsource/polar `caa3e19b` | 1,065 files, 192,219 lines | About 57 feature packages, central `models/`, `kit/`, `integrations/` | Protocols only where providers vary | FastAPI `Depends`; module-level service singletons | 296 edges to remove |
| pypi/warehouse `19127afb` | 288 files, 60,982 lines | 51 feature units | 30 zope interfaces, mostly with a null or local variant | Pyramid service locator | 31 edges to remove |
| pre-commit/pre-commit `a9bba55a` | 67 files, 7,163 lines | Flat modules, `commands/`, `languages/` | One Protocol satisfied by 22 modules | A plain dict registry | None |
| karpathy/nanoGPT `3adf61e1` | 1,220 lines | Flat scripts: `model.py` is the pure core, `train.py` the shell | None | `exec` of config files, which its own docstring calls "Probably a terrible idea" | Not applicable |

None of the four production applications has a persistence-ignorant domain model; services operate on ORM objects. Ports appear where implementations actually vary: Warehouse storage backends and null variants, Dispatch plugins, Polar migration sources and tax providers, pre-commit languages. Feature packaging bounds where a change lands, not how big a module grows: Polar's largest service modules reach 3,000 to 4,500 lines.

Seven "DDD" or "clean architecture" template repositories on GitHub (330 to 1,045 stars) were also inspected. All are teaching examples or starter templates, three say so in their README, and they share the failure modes the stop rules target: every use case as an ABC plus an `Impl` subclass plus a factory; 84 empty files in one, 30 and 29 in two others; a health check spread over 21 files; a `BaseService` forwarding every call through an `Any`-typed repository behind a container; a `seedwork/` three times the size of the richest domain module. The one worth imitating in miniature gives each of its five ports a second implementation and leaves its CRUD module as five flat files.

The Pydantic domain sample was measured on Python 3.14.7 and Pydantic 2.13.5: 0.34 µs per frozen `BaseModel` construction against 0.18 µs for a frozen dataclass, which matters only for millions of objects in a hot loop.

## Sources

Accessed 2026-09-29.

- Martin Fowler, [PresentationDomainDataLayering](https://martinfowler.com/bliki/PresentationDomainDataLayering.html) (2015), [AnemicDomainModel](https://martinfowler.com/bliki/AnemicDomainModel.html) (2003), [DomainDrivenDesign](https://martinfowler.com/bliki/DomainDrivenDesign.html) (2020), [MonolithFirst](https://martinfowler.com/bliki/MonolithFirst.html) (2015).
- Alistair Cockburn, [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture) (2005); Juan Manuel Garrido de Paz, [Hexagonal Architecture](https://jmgarridopaz.github.io/content/hexagonalarchitecture.html) (2018). The 2024 book by both was not read.
- Robert C. Martin, [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) (2012); Jeffrey Palermo, [The Onion Architecture](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/) (2008).
- Eric Evans, [Domain-Driven Design Reference](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf) (2015); Vaughn Vernon, [Effective Aggregate Design](https://www.dddcommunity.org/wp-content/uploads/files/pdf_articles/Vernon_2011_1.pdf) (2011).
- Harry Percival and Bob Gregory, [Architecture Patterns with Python](https://www.cosmicpython.com/) and its [book source](https://github.com/cosmicpython/book) at `d4522c44` (2025-09-08): chapters 2, 3, 4, 6, 7, 8, 9, 13, and the epilogue.
- Jimmy Bogard, [Vertical Slice Architecture](https://www.jimmybogard.com/vertical-slice-architecture/) (2018); Gary Bernhardt, [Functional Core, Imperative Shell](https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell) (2012); Kamil Grzybek, [Modular Monolith: A Primer](https://www.kamilgrzybek.com/blog/posts/modular-monolith-primer) (2019); David Seddon, [How we organise our very large Python monolith](https://blog.europython.eu/kraken-technologies-how-we-organize-our-very-large-pythonmonolith/) (2023).
- Hynek Schlawack, [Don't Mock What You Don't Own in 5 Minutes](https://hynek.me/articles/what-to-mock-in-5-mins/) (2022), [Subclassing in Python Redux](https://hynek.me/articles/python-subclassing-redux/) (2021); [svcs](https://svcs.hynek.me/en/stable/why.html) 26.2, [dishka](https://dishka.readthedocs.io/en/stable/) 1.10, [dependency-injector](https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html) 4.49 documentation.
- [import-linter](https://github.com/seddonym/import-linter/tree/main/docs) 2.15 contract types (`acyclic_siblings` since 2.6, `protected` since 2.5); [Python typing](https://docs.python.org/3/library/typing.html) on `Protocol` and `runtime_checkable`.
- Skeptics: Mark Seemann, [Interfaces are not abstractions](https://blog.ploeh.dk/2010/12/02/Interfacesarenotabstractions/) (2010); Sandi Metz, [The Wrong Abstraction](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction) (2016); Oren Eini, [Repository is the new Singleton](https://ayende.com/blog/3955/repository-is-the-new-singleton) (2009).

The decision-table thresholds ("about 500 lines", "fits on one screen") are this pack's choices aligned with its existing module reminder, not measured constants. Evans', Vernon's, and Martin's books and Bernhardt's screencast were represented by their reference texts and abstracts, not read in full.
