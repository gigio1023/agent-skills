#!/usr/bin/env python3
"""Mechanical pre-release checks for a LaTeX paper.

Follows \\input and \\include from the root file, strips comments, optionally
scans a build log, and reports findings as ``severity<TAB>file:line<TAB>message``. Exit code 1 when any
error was found, 0 otherwise, 2 on bad usage. Python 3.10+, standard library only.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CONFLICT = re.compile(r"^(<<<<<<<|=======|>>>>>>>)")
TODO = re.compile(r"\b(TODO|FIXME|XXX)\b")
TODO_MACRO = re.compile(r"\\(todo|fixme)\b")
WORD = re.compile(r"[A-Za-z][A-Za-z'-]*")
INPUT = re.compile(r"\\(?:input|include)\{([^}]+)\}")
TITLE = re.compile(r"\\title(?:\[[^\]]*\])?\{(.*?)\}", re.S)
ABSTRACT = re.compile(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", re.S)
DOUBLE_DOT = re.compile(r"(?<!\.)\.\.(?!\.)")
LOG_WORDS = re.compile(r"\b(error|warning|undefined|missing)\b", re.I)
ACK = re.compile(r"acknowledg", re.I)


def strip_comment(line: str) -> str:
    out = []
    escaped = False
    for ch in line:
        if ch == "%" and not escaped:
            break
        out.append(ch)
        escaped = ch == "\\" and not escaped
    return "".join(out)


def collect_files(root: Path) -> list[Path]:
    seen: list[Path] = []
    stack = [root.resolve()]
    while stack:
        p = stack.pop()
        if p in seen or not p.is_file():
            continue
        seen.append(p)
        text = p.read_text(encoding="utf-8", errors="replace")
        for m in INPUT.finditer(text):
            target = m.group(1).strip()
            cand = (p.parent / target)
            if cand.suffix == "":
                cand = cand.with_suffix(".tex")
            if not cand.exists():
                alt = (root.parent / target)
                cand = alt.with_suffix(".tex") if alt.suffix == "" else alt
            if cand.exists():
                stack.append(cand.resolve())
    return seen


def check(root: Path, blind: bool, authors: list[str]) -> tuple[list[tuple[str, str, str]], str, str]:
    findings: list[tuple[str, str, str]] = []
    title = ""
    abstract = ""
    for f in collect_files(root):
        raw = f.read_text(encoding="utf-8", errors="replace")
        m = TITLE.search(raw)
        if m and not title:
            title = " ".join(m.group(1).split())
        m = ABSTRACT.search(raw)
        if m and not abstract:
            abstract = " ".join(strip_comment(l) for l in m.group(1).splitlines())
            abstract = " ".join(abstract.split())
        rel = str(f)
        for n, line in enumerate(raw.splitlines(), 1):
            if CONFLICT.match(line):
                findings.append(("error", f"{rel}:{n}", "merge-conflict marker"))
            code = strip_comment(line)
            comment = line[len(code):]
            if ACK.search(comment) and re.search(r"\\(section\*?|paragraph|begin)", comment):
                findings.append(("warning", f"{rel}:{n}", "acknowledgments section appears commented out"))
            if not code.strip():
                continue
            if TODO.search(code):
                findings.append(("error", f"{rel}:{n}", "TODO/FIXME/XXX text"))
            if TODO_MACRO.search(code):
                findings.append(("error", f"{rel}:{n}", "author note macro (\\todo)"))
            words = WORD.findall(code)
            for a, b in zip(words, words[1:]):
                if a.lower() == b.lower() and len(a) > 1:
                    findings.append(("warning", f"{rel}:{n}", f"doubled word: {a} {b}"))
            if DOUBLE_DOT.search(code):
                findings.append(("warning", f"{rel}:{n}", "'..' that is not an ellipsis"))
            if "??" in code:
                findings.append(("warning", f"{rel}:{n}", "'??' (unresolved reference?)"))
            if blind:
                for name in authors:
                    if name and name.lower() in code.lower():
                        findings.append(("error", f"{rel}:{n}", f"author name present in blind submission: {name}"))
    return findings, title, abstract


def scan_log(log: Path) -> list[tuple[str, str, str]]:
    """Report build-log lines containing error, warning, undefined, or missing."""
    out: list[tuple[str, str, str]] = []
    for n, line in enumerate(log.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        words = {w.lower() for w in LOG_WORDS.findall(line)}
        if words:
            sev = "error" if words & {"error", "undefined"} else "warning"
            out.append((sev, f"{log}:{n}", f"build log: {line.strip()[:160]}"))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Mechanical pre-release checks for a LaTeX paper.")
    ap.add_argument("root", help="root .tex file")
    ap.add_argument("--blind", action="store_true", help="fail if any --author name appears in the text")
    ap.add_argument("--author", action="append", default=[], help="author name to search for with --blind (repeatable)")
    ap.add_argument("--log", help="LaTeX build log to scan for error/warning/undefined/missing")
    args = ap.parse_args(argv)
    root = Path(args.root)
    if not root.is_file():
        print(f"usage error: {root} is not a file", file=sys.stderr)
        return 2
    if args.blind and not args.author:
        print("usage error: --blind needs at least one --author", file=sys.stderr)
        return 2
    findings, title, abstract = check(root, args.blind, args.author)
    if args.log:
        log = Path(args.log)
        if not log.is_file():
            print(f"usage error: {log} is not a file", file=sys.stderr)
            return 2
        findings.extend(scan_log(log))
    # A backslash inside an f-string expression needs Python 3.12; keep it outside.
    shown_title = title or "(no \\title found)"
    print(f"info\t{root}\ttitle: {shown_title}")
    if abstract:
        macros = re.findall(r"\\[A-Za-z]+", abstract)
        sev = "warning" if macros else "info"
        note = f" (macros: {', '.join(sorted(set(macros)))})" if macros else ""
        print(f"{sev}\t{root}\tabstract{note}: {abstract[:300]}")
    for sev, loc, msg in findings:
        print(f"{sev}\t{loc}\t{msg}")
    errors = sum(1 for s, _, _ in findings if s == "error")
    warnings = sum(1 for s, _, _ in findings if s == "warning")
    print(f"summary\t{root}\t{errors} error(s), {warnings} warning(s), {len(collect_files(root))} file(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
