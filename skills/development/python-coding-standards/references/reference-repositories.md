# Reference Repositories

Read this when a rule in this skill needs its evidence, when deciding whether a large function or module has a precedent, or when refreshing the thresholds. Nine widely used Python packages were cloned and measured on 2026-09-29; the function and module rules in [functions and modules](functions-and-modules.md) rest on these numbers. Measured figures come from `ast`-based scripts and Ruff 0.16.5; quoted lines were read in the clone at the commit listed.

## Contents

- Repositories and commits
- What the numbers say
- Practices the rules are drawn from
- Quoted explanations
- What not to imitate
- Limits of this evidence

## Repositories and commits

| Repository | Commit | Kind |
| --- | --- | --- |
| openai/openai-python | `68b173a24fa9ebfc6b84694a39a0dd0f9a1e6087` | Generated SDK with handwritten `lib/` |
| anthropics/anthropic-sdk-python | `a7285e919ab79998d9380b3b57f6315b7860b8d8` | Generated SDK with handwritten `lib/` and a `CLAUDE.md` house style |
| stripe/stripe-python | `0f1daf3e54eb5b99abd257b2057189767f3ce7c1` | Generated SDK with handwritten transport and request pipeline |
| encode/httpx | `b5addb64f0161ff6bfe94c124ef76f6a1fba5254` | Handwritten HTTP client, sync and async |
| fastapi/fastapi | `a3d205bf19640528718cb4f05ab77f4dfca6ad9a` | Web framework |
| pydantic/pydantic | `bb6da4cfbb1f559885ea2fa207ec93853bfeac64` | Validation library with `_internal/` |
| python-attrs/attrs | `8f767776326faaed11e6c2974798787f6e19b343` | Class-building library |
| hynek/structlog | `73393f34b40c15688b3fdd0982889b225f11b59b` | Logging library that enforces function-size lint |
| pallets/click | `06b2a678741131fd577ce170e23e5ca0aeba0309` | CLI framework |

Generated files (Stainless, Castiron, and Stripe's OpenAPI output) were measured separately and excluded from function statistics. Tests, examples, and vendored code were excluded.

## What the numbers say

Function bodies are short everywhere, including inside very large files. Body lines run from the first statement after the docstring to the end of the function; `@overload` stubs are excluded.

| Package | Functions | Body median | Body p90 | Over 50 lines | Over 100 lines | Args p90 |
| --- | --- | --- | --- | --- | --- | --- |
| openai (core and `lib/`) | 1,028 | 4 to 6 | 20 to 29 | 2.9% to 4.6% | 1.0% | 3 |
| anthropic (core and `lib/`) | 1,236 | 4 to 5 | 19 to 33 | 2.6% to 5.0% | 0.6% to 0.9% | 3 |
| stripe handwritten | 406 | 6.5 | 23 | 3.4% | 0.5% | 5 |
| httpx | 446 | 5 | 22 | 1.8% | 0.2% | 4 |
| fastapi | 387 | 7 | 32 | 5.4% | 2.1% | 18 |
| pydantic (without `v1/`, `deprecated/`) | 1,130 | 5 | 31 | 4.2% | 1.2% | 3 |
| attrs | 215 | 6 | 37 | 6.0% | 2.3% | 4 |
| structlog | 349 | 2 | 16 | 1.7% | 0.6% | 3 |
| click | 546 | 5 | 30 | 3.8% | 0.4% | 3 |

Parameter median is 1 in every package. A function past 50 body lines sits at about the 95th to 98th percentile of these packages; past 100 lines, at the 99th or above. Functions over 12 branches are 0% to 2.4% and over 50 statements 0% to 1.9%; structlog reaches 0% because it enforces Ruff's PLR0911, PLR0912, and PLR0915 at their defaults and passes.

Files are a different story. 48% to 70% of each library's lines sit in files over 1,000 lines, and the largest handwritten files run 1,000 to 3,900 lines (`click/core.py`, `attrs/_make.py`, `pydantic/_internal/_generate_schema.py`, `httpx/_client.py`). Inside those files, code lines per function stay at 12 to 19 and the largest function holds a median 6% to 13% of the file. In the SDKs, 48% to 85% of the largest files is a mirrored sync and async class pair. A large module here is many small units around one concept, never one function that carries the file.

Complexity lint is not how these projects control size: only structlog enables the PLR09 rules, pydantic configures a C901 threshold without selecting the rule, and none enables Ruff's docstring rules except pydantic (`D1` and `D417`, Google convention). All run a strict type checker on the package (pyright strict, mypy strict, or ty), and the newer SDKs check the public surface in CI.

Local variable annotation is rare: 0% to 17% of first bindings, and roughly half of those are empty containers or `None` initializations a checker cannot infer. This skill's all-locals rule is a readability rule for readers without a language server, especially around external-library values, and does not cite these packages. Return annotations are 94% to 100% everywhere except stripe (62%) and attrs (types live in `.pyi` stubs).

## Practices the rules are drawn from

- **Pure core, thin I/O shells.** `anthropic/_utils/_prepare.py` walks request params once in a pure `copy_tree` and defers file reads to a second phase, "the only step in which `prepare_request_data` and `async_prepare_request_data` differ"; the sync and async entry points are six lines each. `httpx.BaseClient` owns URL, header, cookie, redirect, and auth logic; `Client` and `AsyncClient` only send. `httpx.Auth.auth_flow` is one generator driven by both a sync and an async runner. The counterexample on the same template, `openai/_utils/_transform.py`, keeps two 64-line walks that differ only by `await`.
- **Extract for a named reason and write it down; inline a helper whose name adds nothing to its body.** `anthropic/lib/tools/_skills.py` opens with "Split out from `agent_toolset` because fetching a session agent's skills and safely unpacking a (possibly third-party) archive is a distinct concern"; `lib/_retry.py` was "Extracted so the control-plane poller, the session tool runner, and the worker heartbeat all compute backoff … the same way"; `click/_termui_impl.py` exists "To keep the import time of Click down"; `structlog/exceptions.py` was "factored out to avoid import loops". The Anthropic house style says "Inline a helper that has one caller. Keep one helper when the same logic appears twice," and the same repository extracts single-caller steps with their own contract, such as `_attempt_request`; the deciding question is whether the name and signature add something the body does not, not the number of callers.
- **A private helper sits next to its only caller.** `structlog._make_stamper` directly follows `TimeStamper`; click's private helpers open `core.py` above the classes that use them.
- **Dispatch tables and decide-once construction instead of growing `elif` chains.** `pydantic/_internal/_generate_schema.py` maps types to handlers in two class-level dicts and names one method per case `_<kind>_schema`; `structlog.TimeStamper.__init__` picks one of six closures once so `__call__` is one line.
- **Long functions that survive have one shape.** A flat dispatch with guard returns and a contract docstring (`openai/lib/responses_websocket/_accumulator.py`, 184 lines); a parser split into titled phases (`httpx/_urlparse.py`, 128 lines); or one resource lifetime whose every ordering decision carries a comment naming the failure it prevents (`anthropic/lib/environments/_worker.py`, 207 lines). The worst-measured unit in the set, fastapi's per-request closure at nesting depth 7 and McCabe 49, is the one that narrates its steps in comments.
- **Named records between steps, not tuples.** `anthropic/lib/middleware/_fallbacks.py` passes private `BaseModel` records with a docstring per field between hops; `httpx.urlparse` returns a `NamedTuple`. Stripe's request-preparation step returns an unannotated 8-tuple that two callers unpack by position.
- **Wide signatures are keyword-only.** Among functions with more than five parameters, at least half are keyword-only in 96% to 100% of openai and anthropic functions and 82% of httpx; the older stripe and click APIs stay positional for compatibility.
- **Private by file, public by explicit re-export, ordered by importance.** 76% to 98% of handwritten SDK modules carry a `_` prefix; stripe rejects a new non-private module with a lint rule; openai and anthropic detect public-surface changes with griffe in CI. pydantic pairs each public module with an `_internal/` mechanism module (`fields.py` with `_internal/_fields.py`). Two export forms are recognized by type checkers: `__all__` (pydantic, attrs, structlog, httpx) and `from .x import Name as Name` (click, fastapi). The Anthropic house style: "Order a file by importance. The classes a reader came for go at the top, and small internal helpers go at the bottom."
- **Leaf modules for shared vocabulary.** pydantic has no runtime import cycle across 79 modules; its `errors` and `warnings` modules import nothing from the package and are imported by 23 and 18 modules. Cycles closed through the package root (`fastapi/utils.py`, `structlog/contextvars.py`) work only because attributes are read at call time.
- **One exception root, subclasses by caller action, one translation seam, fields instead of message parsing.** httpx maps every transport exception inside `map_httpcore_exceptions()`; the SDKs translate timeouts and connection failures in one request step and status codes in one factory, chain with `from err`, and carry `status_code`, `request_id`, `body`, and the like as fields. Anthropic's rule: package errors for SDK logic, builtins such as `TypeError` for plain misuse, and "Never tell cases apart by matching text." Retry loops catch a named tuple of transient errors, not `Exception`, because that "would also retry programming errors".
- **The underscore decides documentation obligation.** Public functions carry docstrings in 82% to 96% of pydantic, attrs, and structlog; private helpers whose name and signature say everything have none (`_get_first_arg_or_any`, `_impartial`). pydantic's Ruff configuration and its API-docs filter both skip underscore names.
- **Validated models at the boundary, plain records inside, in frameworks.** fastapi uses `BaseModel` for its OpenAPI document and credentials and dataclasses for internal dependency records; attrs' documentation calls Pydantic "the right tool for Commands" and argues against re-validating trusted objects in the domain layer. Both are libraries shipping into other people's dependency trees, which is the case this pack reserves for dataclasses; an application that already depends on Pydantic keeps one model per meaning. [Pydantic integration](pydantic-integration.md) states the split.

## Quoted explanations

Comments and docstrings that explain what code cannot show:

- Ordering with the failure it prevents, `anthropic/lib/environments/_worker.py`: "Start the lease heartbeat BEFORE entering AgentToolContext. AgentToolContext.__aenter__ downloads and extracts every skill the session agent has; that can take longer than the lease TTL. If the first heartbeat only fired after the download (the old ordering), a slow download would let the lease lapse and another worker reclaim the item — both workers then serve the same session (split-brain)."
- Step-helper contract, `anthropic/_base_client.py`: "Prepare, build and send a single HTTP attempt. Returns the response regardless of its status code, along with the prepared options it was sent with — status handling (the retry policy, raising typed errors for the caller) happens above, where middleware can inspect error responses first."
- Branch order, `pydantic/_internal/_generate_schema.py`: "this must come before the `is_namedtuple()` check as enums values can be namedtuples".
- Environmental constraint, `stripe/_http_client.py`: HTTP libraries are detected at import "so the expensive imports … happen during Python's init phase rather than when StripeClient() is constructed. This matters in environments like AWS Lambda where module loading has a generous timeout (10s) but handler invocation does not (often 3s)."
- Why a sentinel and not `None`, `httpx/_client.py`: "Omitting the `timeout` parameter will send a request using whatever default timeout has been configured on the client. Including `timeout=None` will ensure no timeout is used."
- Representation with its cost, `anthropic/_utils/_prepare.py`: "A plain tuple rather than a NamedTuple, as one is created for every value visited".
- Error field that removes message parsing, `anthropic/_exceptions.py`: "`path` is the file the provider tried to read (when known), so callers waiting for a projected token to appear can retry without parsing the message."
- Compatibility path kept on purpose, `attrs/_make.py`: `_collect_base_attrs_broken` documents "Adhere to the old incorrect behavior" and links the issue.
- Test seam named as such, `structlog/_frames.py`: `_getframe` is "Only for testing to avoid monkeypatching of sys._getframe."

## What not to imitate

These shapes exist because of generator ownership, import cost at library scale, or compatibility promises, and an application does not share the reason:

- Generated method shapes: triple `@overload` per method with 20 to 30 keyword parameters and per-parameter spec text, repeated for sync and async and wrapped again for raw and streaming responses (`openai/resources/responses/responses.py`, 5,347 lines). fastapi's per-verb documented signatures (3,557 of `routing.py`'s 6,447 lines) serve editor tooltips the same way.
- One file per schema type (openai: 1,779 generated files, median 34 lines). Tooling navigates them; handwritten code split this way scatters one responsibility.
- Whole-class sync and async copies where the logic is not shared (`openai/lib/streaming/_assistants.py`, two 143-line dispatchers).
- Lazy import maps, module `__getattr__`, and `__module__` rewriting in the package root (stripe, pydantic, httpx). Justified by import cost at that module count, not by an ordinary application.
- Module-level mutable configuration (`stripe.api_key`).
- Positional multi-argument error constructors and tuple returns (stripe); positional signatures with 12 to 25 parameters kept for compatibility (click, attrs).
- Runtime code generation, metaclass construction, parallel `.pyi` stubs over untyped source, dual Pydantic v1 and v2 support, version-migration shims, and suppressions for a rule that is not enabled (pydantic's eleven `# noqa: C901` with `C90` unselected).
- Import cycles closed through the package root, and a per-request closure at nesting depth 7 with step-narrating comments (fastapi `routing.py`).

## Limits of this evidence

Shallow clones give no history, so the reports cannot show how large files grew or whether splits happened for the reasons their docstrings give. Generated versus handwritten classification is heuristic for the Stainless-lineage SDKs, whose core files mix template output and hand patches. Body-line counts include comments and blank lines. All nine are libraries or frameworks: application trade-offs such as validation cost, dependency weight, and domain isolation differ, which matters most for the Pydantic-first question. Anthropic's `CLAUDE.md` states rules its code does not fully follow yet (no dataclasses, no second underscore inside private files); those lines are quoted as policy, not as observed practice.
