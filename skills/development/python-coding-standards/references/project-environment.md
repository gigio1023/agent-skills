# Project Environment

Read this when setting up Python, changing dependencies, or arranging local and CI commands. Prefer uv project management; this is not a pip-based installation recipe.

## Project files and scope

For new Python projects, select a supported Python version at least 3.12 that fits deployment and dependencies. Initialize only inside the intended project, and keep `project.requires-python`, the selected development interpreter, and CI consistent. In an existing project, inspect its metadata, lockfile, workspace, and automation before changing them; an incidental code fix does not authorize replacing its package manager or dropping older Python support. Identify a conflicting requirement explicitly.

Use `uv python pin <version>` when the project should persist its development interpreter in `.python-version`. The supported range in `requires-python` and the selected development version serve different purposes; `--python` on one command does not itself pin later commands. Do not assume the newest local interpreter matches the project's intended test runtime.

Use `pyproject.toml` for declared dependencies and configuration, and generate `uv.lock` through uv. Keep the lockfile in version control for the managed project; do not commit `.venv/`. Do not hand-edit resolved packages in the lockfile. Add or remove dependencies through `uv add` and `uv remove`, and keep their constraints deliberate rather than upgrading unrelated packages.

## Dependency groups

Put runtime requirements in `project.dependencies` under `[project]`. Use `[dependency-groups]` for tools used to develop and check the project, such as `test` and `lint`, adding separate groups only when they serve distinct commands or environments. Do not put development-only tools into runtime requirements or publish them as optional features by accident. `[project.optional-dependencies]` is for extras that consumers select, not the default home for test and lint tools.

For a project that uses pytest and Ruff, the relevant operations are:

```bash
uv add pydantic
uv add --group test pytest
uv add --group lint ruff
uv sync --group test --group lint
uv run --locked --group test pytest
uv run --locked --group lint ruff check .
```

These are examples, not a requirement to add those tools to an existing project. Reuse its chosen test and lint tools. A `dev` group may include `test` and `lint` with `{ include-group = "test" }` and `{ include-group = "lint" }`. Decide whether groups are selected explicitly or through `tool.uv.default-groups`; keep local and CI commands consistent. Review resolution across groups instead of bypassing incompatibilities with an environment-only install.

## Reproduce the environment

Run project commands through `uv run` and synchronize with `uv sync`. These can update the environment and lockfile; they are not read-only diagnostics. Once dependency changes are intentional and resolved, use `uv lock --check` and locked runs in CI to fail on stale metadata instead of silently relocking. `--frozen` skips the freshness check and is not equivalent to `--locked`.

Use only the groups needed by the environment. When a deployment should exclude every development group, account for configured defaults rather than assuming `--no-dev` disables all of them. Do not let a test-only dependency become an undeclared runtime dependency because it happens to exist locally.

## Exceptional environments

Do not use `pip install` or `uv pip install` for ordinary setup, dependency changes, or failed-resolution recovery. Missing uv, a resolver error, and convenience alone do not justify either command. Check whether a compatible uv project workflow is available; if setup authority or a prerequisite is missing, report it rather than silently installing a global tool.

A narrowly scoped external environment that cannot consume the project workflow can justify an exception. State the concrete restriction and keep a reproducible dependency source, preferably derived from the project metadata and lockfile, instead of making ad hoc installs the source of truth. Do not use transient `uv run --with` dependencies to conceal missing declarations for normal project commands.

## Sources

Checked 2026-09-10:

- [uv projects](https://docs.astral.sh/uv/guides/projects/): project files, interpreter selection, and command execution.
- [uv dependency management](https://docs.astral.sh/uv/concepts/projects/dependencies/): project requirements, extras, groups, includes, and default groups.
- [uv locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/): environment updates and locked versus frozen behavior.

Python 3.12+, uv-first setup, explicit group selection, and the restricted pip exception are owner-selected preferences, not universal Python requirements.
