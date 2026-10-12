# Renames

Two packages with the same frontmatter name cannot share the canonical `~/.agents/skills/<name>` directory, and a skill named like a harness built-in command can shadow it or be shadowed. A rename gives one side a prefix and records the choice so every later install or refresh of that source applies it again.

## Renames File

The record lives outside any package, at `~/.agents/skill-pack-renames.json`, so replacing this skill does not erase it. Each key is a normalized source: `host/owner/repo` in lowercase, without a scheme, `.git`, or `#ref`. GitHub shorthand, HTTPS, and SSH forms of one repository share a key, and `scripts/rename_skills.py` normalizes `--source` the same way.

```json
{
  "github.com/example-org/ui-skills": {
    "prototype": "ui-prototype"
  }
}
```

Each entry maps an upstream frontmatter name to its installed name. Write or change an entry only after the user chose that rename; read and preserve the other entries when editing the file.

## Deciding A Collision

Check the selected names against `skills list --global --json` and against the built-in commands of the target harnesses. A name that only matches a package from the same source is a refresh, not a collision.

When a name collides, ask the user which side takes a prefix and which prefix to use. A built-in command cannot be renamed, so the choice there is between prefixing the incoming skill and installing it under its own name. Keeping both under one name is not an option for two skill packages; the second install would overwrite the first. Record the decision before writing packages.

## Writing Renamed Packages

Run the script from this skill's directory against the reviewed checkout, with the selection by upstream names and a new output directory:

```bash
python3 scripts/rename_skills.py "$review_dir/repo" \
  --source "$source_repo" \
  --out "$review_dir/renamed" \
  --skill <upstream-name> --skill <upstream-name>
```

The script reads the source's entry from the renames file; `--rename OLD=NEW` adds or overrides pairs for a first run before the entry is written. It changes only these forms of an old name in the selected packages:

- the renamed package's frontmatter `name` and folder;
- a slash command, `/old`, not part of a path or URL;
- a tool call, ``Skill tool with "old"`` or with backticks or single quotes;
- a reference, ``the `old` skill``;
- an exact backticked name, `` `old` ``, which in prose such as ``run `old` first`` names that skill.

Its JSON summary lists `written` packages (renamed, or rewritten because they invoke or reference an old name), `unchanged` packages, each changed line, and `review` lines that quote an old name in another way. Read every changed line and every review line. A backticked skill name in prose is usually a reference to that skill and should carry the new name; if a changed line used the backticked name for something else, such as a literal value or an unrelated identifier, restore it in the output. Judge the remaining review lines, which quote an old name another way, case by case: edit a line that points at the renamed skill and leave a label or ordinary word as written. When such an edit falls in a package listed as `unchanged`, copy that package into `<out>/skills/<name>` first and install it with the `written` packages. Include every manual edit in the source review. The script exits with status 2 when an old name is absent from the source, a new name already belongs to another package in the source, a selected name is unknown, or the output directory is not empty.

## Installing And Recording

Install `unchanged` packages from the remote source and `written` packages from the output directory, as the main procedure describes. A package that only references a renamed skill comes from the output directory too, so its invocation keeps pointing at the right package.

After verification passes:

- Write the decided entry into the renames file.
- When the rename replaces a name that an earlier install of the same source left in place, compare that old canonical package with the reviewed revision before removing it. Remove it with `npx --yes "skills@$skills_cli_version" remove <old-name> --global --yes` only when the user asked for this rename, and surface any local edits first.
- Report that the renamed and rewritten packages now refresh only through this skill, because the CLI records their source as a local path that later disappears.
