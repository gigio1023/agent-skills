#!/usr/bin/env python3
"""Verify that Python changes are limited to docstrings and ordinary comments."""

from __future__ import annotations

import argparse
import ast
from collections import Counter
import io
from pathlib import Path
import re
import subprocess
import sys
import tokenize


DIRECTIVE_RE = re.compile(
    r"^#(?:!|\s*(?:"
    r"coding\s*[:=]|"
    r"type\s*:|"
    r"noqa\b|"
    r"fmt\s*:|"
    r"ruff\s*:|"
    r"pylint\s*:|"
    r"pyright\s*:|"
    r"mypy\s*:|"
    r"isort\s*:|"
    r"coverage\s*:|"
    r"pragma\s*:\s*no\s+cover\b"
    r"))",
    re.IGNORECASE,
)


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
            return body[1:]
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


def run_git(*args: str, cwd: Path) -> bytes:
    """Run Git and return stdout, raising a readable error on failure."""

    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
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
    """Return an attribute-free AST dump without standard docstrings."""

    try:
        tree = ast.parse(source, filename=label, type_comments=True)
    except SyntaxError as exc:
        raise ValueError(f"{label}: syntax error: {exc}") from exc
    stripped = DocstringStripper().visit(tree)
    ast.fix_missing_locations(stripped)
    return ast.dump(stripped, annotate_fields=True, include_attributes=False)


def semantic_directives(source: str, label: str) -> Counter[str]:
    """Collect comments that can affect interpreters or development tools."""

    try:
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        directives = [
            token.string.strip()
            for token in tokens
            if token.type == tokenize.COMMENT and DIRECTIVE_RE.match(token.string.strip())
        ]
    except (IndentationError, tokenize.TokenError) as exc:
        raise ValueError(f"{label}: tokenization failed: {exc}") from exc
    return Counter(directives)


def repository_root() -> Path:
    """Return the current Git repository root."""

    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
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
        f"OK: {len(args.files)} file(s) contain only standard docstring/comment changes "
        f"relative to {args.base}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
