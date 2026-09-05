# Validator Contract

Run the helper; do not load it as model instructions. It requires Python 3.10+ and PyYAML (verified with 6.0.3). The Bash command delegates to the Python entry point. Dependencies are never installed automatically.

From the package root:

```bash
bash scripts/validate_skill.sh .
bash scripts/smoke_test.sh
# With an authorized isolated dependency environment:
uv run --with PyYAML==6.0.3 bash scripts/validate_skill.sh .
uv run --with PyYAML==6.0.3 bash scripts/smoke_test.sh
```

Use SKILL_BUILDER_PYTHON to select an existing Python environment. The Python entry point takes a package directory and optional --target claude-code. The default target is portable. These profiles are scoped static checks, not complete host implementations or a replacement for live discovery.

## Errors

- Missing/unreadable SKILL.md, malformed UTF-8 or YAML, duplicate metadata keys.
- Invalid required field types, documented lengths, name syntax or directory identity; malformed standard optional metadata.
- Broken direct Markdown links from SKILL.md, or packaged links escaping the package. Parent-relative links inside the package are valid.
- Packaged symlinks that are broken or resolve outside the package.
- For the optional Anthropic target: reserved names and XML tags in metadata.

Errors return 1. Missing dependencies or invalid CLI use return 2. Otherwise return 0, even if advisories are printed.

## Advisories

- A SKILL.md file over 500 lines, a long reference without a contents map, native/unknown metadata, and experimental allowed-tools.
- Unfinished-looking markers or machine-specific paths in prose.
- Private-reasoning terminology requiring human review; prohibitions also match.
- Missing code-span resources or links inside supporting Markdown: these may describe generated outputs, optional downloads, or a vendored source's layout. Inspect the context and fix actual execution defects; do not silently dismiss the warning or require every optional dependency just to validate a package.

There is no 8KB warning, token estimate, required Gotchas section, or rejection of intentional reference cross-links. Optional metadata is not itself an error.

## Coverage Limits

YAML uses PyYAML's safe loader and YAML 1.1 scalar resolution; quote values such as on/off or numeric-looking names when they must remain strings. Duplicate mapping keys are rejected as a local ambiguity check. YAML aliases are not executed. Host-specific configuration schemas and agents/openai.yaml are not validated.

The link checker inspects all packaged Markdown files outside fenced code and inline code spans. It recognizes ordinary inline links, reference definitions, and code-span paths beginning references/, scripts/, or assets/. Escaped paths, nested-parenthesis destinations, dynamic paths, other Markdown extensions, and links inside code examples need manual review. It does not check anchors or fetch external URLs. Empty directories and unreferenced assets are allowed.

No package script, template, hook, or downloaded content is executed by linting. Link existence does not prove resource quality or safe execution. Inspect commands, effects, dependencies, and target behavior separately.

The smoke suite tests the checker with temporary local files, including valid long skills, optional metadata, malformed YAML, and broken/escaping resources. It is ordinary software regression testing, not a model benchmark.
