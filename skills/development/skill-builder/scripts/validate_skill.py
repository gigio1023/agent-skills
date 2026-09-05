#!/usr/bin/env python3
"""Static Agent Skills package checks; see references/validation.md."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

try:
    import yaml
except ImportError:
    print("SETUP: PyYAML is missing. Use an existing environment or, when authorized,\n"
          "uv run --with PyYAML==6.0.3 python scripts/validate_skill.py <skill-dir>",
          file=sys.stderr)
    raise SystemExit(2)


class UniqueSafeLoader(yaml.SafeLoader):
    """Safe YAML with explicit duplicate-key rejection."""

    def construct_mapping(self, node, deep=False):
        self.flatten_mapping(node)
        result = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                duplicate = key in result
            except TypeError as exc:
                raise yaml.constructor.ConstructorError(
                    None, None, "unhashable mapping key", key_node.start_mark
                ) from exc
            if duplicate:
                raise yaml.constructor.ConstructorError(
                    None, None, f"duplicate key: {key!r}", key_node.start_mark
                )
            result[key] = self.construct_object(value_node, deep=deep)
        return result


def unfenced(text: str) -> str:
    """Remove backtick/tilde fences, preserving longer outer fences."""
    result = []
    fence = None
    for line in text.splitlines():
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if (match and match[1][0] == fence[0] and
                    len(match[1]) >= fence[1] and not match[2].strip()):
                fence = None
            continue
        if match:
            fence = (match[1][0], len(match[1]))
        else:
            result.append(line)
    return "\n".join(result)


def destinations(text: str) -> set[tuple[str, bool]]:
    """Recognize common links, definitions and literal packaged code paths."""
    visible = unfenced(text)
    spans = re.findall(r"(`+)(.+?)\1", visible)
    paths = {
        (value, True) for _, value in spans
        if re.fullmatch(r"(?:references|scripts|assets)/[^\s`*<>]+\.[\w-]+", value)
    }
    prose = re.sub(r"(`+).+?\1", "", visible)
    patterns = [
        r"\]\(\s*(?:<([^>\n]+)>|([^\s()]+))(?:\s+[\"'][^\"']*[\"'])?\s*\)",
        r"(?m)^ {0,3}\[[^\]\n]+\]:\s*(?:<([^>\n]+)>|([^\s]+))",
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, prose):
            paths.add((match[1] or match[2], False))
    return paths


def validate(package: Path, target: str = "portable") -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    package = package.resolve()
    entry = package / "SKILL.md"
    if not entry.is_file():
        return ["missing SKILL.md"], warnings

    # Do not follow an escaping entry/resource while performing static checks.
    for path in package.rglob("*"):
        if path.is_symlink():
            try:
                resolved = path.resolve(strict=True)
                if not resolved.is_relative_to(package):
                    errors.append(f"symlink escapes package: {path.relative_to(package)}")
            except (OSError, RuntimeError):
                errors.append(f"broken or cyclic symlink: {path.relative_to(package)}")
    if errors:
        return errors, warnings

    try:
        text = entry.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"cannot read SKILL.md: {exc}"], warnings
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return ["SKILL.md must begin with YAML delimiter ---"], warnings
    try:
        close = lines.index("---", 1)
    except ValueError:
        return ["missing YAML closing delimiter"], warnings
    try:
        metadata = yaml.load("\n".join(lines[1:close]), Loader=UniqueSafeLoader)
    except (yaml.YAMLError, ValueError, RecursionError) as exc:
        return [f"invalid YAML: {exc}"], warnings
    if not isinstance(metadata, dict):
        return ["frontmatter must be a mapping"], warnings

    name = metadata.get("name")
    description = metadata.get("description")
    if not isinstance(name, str) or not 1 <= len(name) <= 64:
        errors.append("name must be a string of 1-64 characters")
    else:
        if (name.startswith("-") or name.endswith("-") or "--" in name or
                any(c != "-" and not (c.isalnum() and c == c.lower()) for c in name)):
            errors.append("name must contain lowercase alphanumerics and single hyphens")
        if name != package.name:
            errors.append(f"name must match directory: {package.name}")
        if target == "claude-code" and any(word in name for word in ("anthropic", "claude")):
            errors.append("Anthropic target disallows reserved words in name")
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        errors.append("description must be a nonempty string of at most 1024 characters")
    elif target == "claude-code" and re.search(r"</?[A-Za-z][^>]*>", description):
        errors.append("Anthropic target disallows XML/HTML tags in description")

    for field in ("license", "compatibility", "allowed-tools"):
        if field in metadata:
            value = metadata[field]
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{field} must be a nonempty string")
            elif field == "compatibility" and len(value) > 500:
                errors.append("compatibility exceeds 500 characters")
    if "metadata" in metadata:
        value = metadata["metadata"]
        if not isinstance(value, dict) or any(
            not isinstance(k, str) or not isinstance(v, str) for k, v in value.items()
        ):
            errors.append("metadata must map strings to strings")
    standard = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
    for key in metadata:
        if not isinstance(key, str):
            errors.append("frontmatter field names must be strings")
        elif key not in standard:
            warnings.append(f"native/unknown field {key!r}: verify its target schema")
    if "allowed-tools" in metadata:
        warnings.append("allowed-tools is experimental; verify target permission semantics")

    body = "\n".join(lines[close + 1:])
    if len(lines) > 500:
        warnings.append(f"SKILL.md has {len(lines)} lines: review retrieval structure (advisory)")
    prose = re.sub(r"(`+).+?\1", "", unfenced(body))
    if re.search(r"\b(?:TODO|FIXME|XXX)\b", prose):
        warnings.append("unfinished-looking marker: inspect context, not automatically invalid")
    if re.search(r"(?:/Users/|/home/|[A-Z]:\\)", prose):
        warnings.append("machine-specific path in prose: review portability")
    if re.search(r"chain[- ]of[- ]thought|private reasoning|hidden reasoning|scratchpad", body, re.I):
        warnings.append("private-reasoning terminology: review context; prohibitions also match")

    for path in sorted(package.rglob("*.md")):
        try:
            content = body if path == entry else path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"cannot read {path.relative_to(package)}: {exc}")
            continue
        file_lines = content.splitlines()
        if path != entry and len(file_lines) > 100:
            if not re.search(r"^#+\s+(?:(?:table of )?contents|toc|목차)\b",
                             "\n".join(file_lines[:100]), re.I | re.M):
                warnings.append(f"{path.relative_to(package)}: consider a contents map or search hints")
        for link, code_literal in sorted(destinations(content)):
            try:
                url = urlsplit(link)
            except ValueError:
                errors.append(f"malformed link in {path.relative_to(package)}: {link}")
                continue
            if url.scheme or url.netloc or not url.path:
                continue
            relative = unquote(url.path)
            # Code-span package paths always resolve from the package root.
            # Ordinary Markdown links resolve from their containing file.
            code_path = relative.startswith(("references/", "scripts/", "assets/"))
            origin = package if code_path and code_literal else path.parent
            try:
                resolved = (origin / relative).resolve()
                if not resolved.is_relative_to(package):
                    errors.append(f"resource escapes package: {path.relative_to(package)} -> {link}")
                elif not resolved.exists():
                    message = f"missing resource: {path.relative_to(package)} -> {link}"
                    if path == entry and not code_literal:
                        errors.append(message)
                    else:
                        warnings.append(message + " (check generated, optional, or source-relative context)")
            except (OSError, RuntimeError) as exc:
                errors.append(f"invalid resource path: {link}: {exc}")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", nargs="?", type=Path, default=Path("."))
    parser.add_argument("--target", choices=("portable", "claude-code"), default="portable")
    args = parser.parse_args()
    errors, warnings = validate(args.skill_dir, args.target)
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"FAIL: {error}")
    if errors:
        return 1
    print(f"OK: {args.skill_dir} static package checks passed (target={args.target})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
