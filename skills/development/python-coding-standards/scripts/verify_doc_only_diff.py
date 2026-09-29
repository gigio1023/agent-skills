#!/usr/bin/env python3
"""Verify that Python changes are limited to docstrings and ordinary comments.

The guard compares each file with a Git revision after removing standard
docstrings, and separately compares the tool directives found in comments.
It cannot see docstring consumers: a module docstring used as an ``argparse``
description or a Pydantic model docstring that becomes a JSON-schema
description changes runtime output while passing here. Check those by hand.
"""

from __future__ import annotations

import argparse
import ast
import io
import re
import subprocess
import sys
import tokenize
from collections import Counter
from pathlib import Path

# Comment segments that tools honor. Ruff, ty, pyrefly, and coverage each find
# their directive anywhere in a comment, so a comment is split at every "#" and
# each segment is tested at its start. Case-insensitive because Ruff and
# coverage accept upper-case spellings of their directives.
DIRECTIVE_RE = re.compile(
    r"^#\s*(?:"
    r"coding\s*[:=]|"
    r"noqa\b|"
    r"fmt\s*:|"
    r"ruff\s*:|"
    r"flake8\s*:|"
    r"isort\s*:|"
    r"yapf\s*:|"
    r"pylint\s*:|"
    r"pyright\s*:|"
    r"mypy\s*:|"
    r"ty\s*:|"
    r"pyrefly\s*:|"
    r"pyre-(?:ignore|fixme)|"
    r"zuban\s*:|"
    r"nosec\b|"
    r"pragma\b"
    r")",
    re.IGNORECASE,
)
# PEP 484 type comments are lowercase. Matching them case-sensitively keeps
# prose such as "# Type: RFC 3339 text" out of the directive count.
TYPE_COMMENT_RE = re.compile(r"^#\s*type\s*:")
SHEBANG_RE = re.compile(r"^#!")


class DocstringStripper(ast.NodeTransformer):
    """Remove standard runtime docstrings while preserving executable nodes."""

    @staticmethod
    def _without_docstring(body: list[ast.stmt]) -> list[ast.stmt]:
        if not body:
            return body
        first = body[0]
        if (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        ):
            body = body[1:]
        # A body that was only "..." or "pass" and a body that was only a
        # docstring behave the same at runtime, so both normalize to empty.
        if len(body) == 1 and _is_placeholder(body[0]):
            return []
        return body

    def visit_Module(self, node: ast.Module) -> ast.AST:  # noqa: N802
        self.generic_visit(node)
        node.body = self._without_docstring(node.body)
        return node

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.AST:  # noqa: N802
        self.generic_visit(node)
        node.body = self._without_docstring(node.body)
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:  # noqa: N802
        self.generic_visit(node)
        node.body = self._without_docstring(node.body)
        return node

    def visit_AsyncFunctionDef(  # noqa: N802
        self, node: ast.AsyncFunctionDef
    ) -> ast.AST:
        self.generic_visit(node)
        node.body = self._without_docstring(node.body)
        return node


def _is_placeholder(statement: ast.stmt) -> bool:
    if isinstance(statement, ast.Pass):
        return True
    return (
        isinstance(statement, ast.Expr)
        and isinstance(statement.value, ast.Constant)
        and statement.value.value is Ellipsis
    )


def run_git(*args: str, cwd: Path) -> bytes:
    """Run Git and return stdout, raising a readable error on failure."""

    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(detail or f"git {' '.join(args)} failed")
    return result.stdout


def decode_python(data: bytes, label: str) -> str:
    """Decode Python source using its declared encoding."""

    try:
        encoding, _ = tokenize.detect_encoding(io.BytesIO(data).readline)
        return data.decode(encoding)
    except (LookupError, SyntaxError, UnicodeDecodeError) as exc:
        raise ValueError(f"{label}: cannot decode Python source: {exc}") from exc


def normalized_ast(source: str, label: str) -> str:
    """Return an attribute-free AST dump without standard docstrings.

    Type comments are deliberately not parsed into the tree: ``TypeIgnore``
    nodes carry their line number as a field, so a docstring added above a
    ``# type: ignore`` line would otherwise count as an executable change.
    ``semantic_directives`` compares those comments by text instead.
    """

    try:
        tree = ast.parse(source, filename=label)
    except SyntaxError as exc:
        raise ValueError(f"{label}: syntax error: {exc}") from exc
    stripped = DocstringStripper().visit(tree)
    ast.fix_missing_locations(stripped)
    return ast.dump(stripped, annotate_fields=True, include_attributes=False)


def semantic_directives(source: str, label: str) -> Counter[str]:
    """Collect comment segments that can affect interpreters or development tools."""

    directives: Counter[str] = Counter()
    try:
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        for token in tokens:
            if token.type != tokenize.COMMENT:
                continue
            comment: str = token.string.strip()
            if token.start[0] == 1 and SHEBANG_RE.match(comment):
                directives[" ".join(comment.split())] += 1
                continue
            segment: str
            for segment in re.split(r"(?=#)", comment):
                if DIRECTIVE_RE.match(segment) or TYPE_COMMENT_RE.match(segment):
                    directives[" ".join(segment.split())] += 1
    except (IndentationError, tokenize.TokenError) as exc:
        raise ValueError(f"{label}: tokenization failed: {exc}") from exc
    return directives


def repository_root() -> Path:
    """Return the current Git repository root."""

    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "not inside a Git repository")
    return Path(result.stdout.strip()).resolve()


def repo_relative(path_arg: str, root: Path) -> tuple[Path, str]:
    """Resolve one input path and its Git-style repository-relative name."""

    path = Path(path_arg)
    current = path.resolve() if path.is_absolute() else (Path.cwd() / path).resolve()
    try:
        relative = current.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{path_arg}: path is outside repository {root}") from exc
    return current, relative.as_posix()


def verify_file(path_arg: str, base: str, root: Path) -> list[str]:
    """Return problems found for one current/base file pair."""

    problems: list[str] = []
    try:
        current_path, relative = repo_relative(path_arg, root)
        if current_path.suffix != ".py":
            return [f"{relative}: expected a .py file"]
        if not current_path.is_file():
            return [f"{relative}: current file does not exist"]

        current_source = decode_python(current_path.read_bytes(), relative)
        base_data = run_git("show", f"{base}:{relative}", cwd=root)
        base_source = decode_python(base_data, f"{base}:{relative}")

        if normalized_ast(current_source, relative) != normalized_ast(
            base_source, f"{base}:{relative}"
        ):
            problems.append(f"{relative}: executable AST changed")

        current_directives = semantic_directives(current_source, relative)
        base_directives = semantic_directives(base_source, f"{base}:{relative}")
        if current_directives != base_directives:
            problems.append(
                f"{relative}: semantic tool directives changed "
                f"(base={dict(base_directives)}, current={dict(current_directives)})"
            )
    except (OSError, RuntimeError, ValueError) as exc:
        problems.append(str(exc))
    return problems


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare current Python files with a Git revision after removing "
            "standard docstrings; fail on executable AST or tool-directive changes."
        )
    )
    parser.add_argument(
        "--base",
        default="HEAD",
        help="Git revision to compare against (default: HEAD)",
    )
    parser.add_argument("files", nargs="+", help="Python files to verify")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        root = repository_root()
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    problems: list[str] = []
    for path_arg in args.files:
        problems.extend(verify_file(path_arg, args.base, root))

    if problems:
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        return 1

    print(
        f"OK: {len(args.files)} file(s) contain only standard docstring or comment "
        f"changes relative to {args.base}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
