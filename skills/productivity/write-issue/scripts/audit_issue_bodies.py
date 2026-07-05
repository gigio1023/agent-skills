#!/usr/bin/env python3
"""Audit GitHub issue bodies for markdown/locale quality gates.

Checks:
- escaped_newline: literal "\\n" / "\\r\\n" / "\\t" exists in body text
- english_heavy: latin chars are dominant and hangul is nearly absent

Exit code:
- 0: no findings
- 2: findings exist
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from typing import List


@dataclass
class Finding:
    repo: str
    number: int
    title: str
    url: str
    escaped_newline: bool
    english_heavy: bool
    latin_chars: int
    hangul_chars: int


def sh_json(cmd: List[str]):
    out = subprocess.check_output(cmd, text=True)
    return json.loads(out)


def is_english_heavy(text: str, latin_min: int, hangul_max: int) -> tuple[bool, int, int]:
    latin = len(re.findall(r"[A-Za-z]", text))
    hangul = len(re.findall(r"[가-힣]", text))
    return latin >= latin_min and hangul <= hangul_max, latin, hangul


def main() -> int:
    p = argparse.ArgumentParser(description="Audit issue bodies for escaped-newline and english-heavy content")
    p.add_argument("--repo", action="append", required=True, help="owner/repo (repeatable)")
    p.add_argument("--author", help="filter issues by GitHub login")
    p.add_argument("--state", default="open", choices=["open", "closed", "all"])
    p.add_argument("--limit", type=int, default=300)
    p.add_argument("--latin-min", type=int, default=80)
    p.add_argument("--hangul-max", type=int, default=10)
    p.add_argument("--json", action="store_true", help="print JSON")
    args = p.parse_args()

    findings: List[Finding] = []

    for repo in args.repo:
        cmd = [
            "gh",
            "issue",
            "list",
            "--repo",
            repo,
            "--state",
            args.state,
            "--limit",
            str(args.limit),
            "--json",
            "number,title,url",
        ]
        if args.author:
            cmd.extend(["--author", args.author])
        issues = sh_json(cmd)

        for it in issues:
            v = sh_json([
                "gh",
                "issue",
                "view",
                str(it["number"]),
                "--repo",
                repo,
                "--json",
                "body",
            ])
            body = (v.get("body") or "").strip()
            escaped = any(x in body for x in [r"\n", r"\r\n", r"\t"])
            eng_heavy, latin, hangul = is_english_heavy(body, args.latin_min, args.hangul_max)
            if escaped or eng_heavy:
                findings.append(
                    Finding(
                        repo=repo,
                        number=it["number"],
                        title=it["title"],
                        url=it["url"],
                        escaped_newline=escaped,
                        english_heavy=eng_heavy,
                        latin_chars=latin,
                        hangul_chars=hangul,
                    )
                )

    if args.json:
        print(
            json.dumps(
                [f.__dict__ for f in findings],
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        if not findings:
            print("No findings")
        else:
            for f in findings:
                flags = []
                if f.escaped_newline:
                    flags.append("escaped_newline")
                if f.english_heavy:
                    flags.append("english_heavy")
                print(f"{f.repo}#{f.number} [{' ,'.join(flags)}] {f.title} -> {f.url}")

    return 2 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
