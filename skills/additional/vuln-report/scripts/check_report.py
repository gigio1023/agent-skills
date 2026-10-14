#!/usr/bin/env python3
"""Flag passages in a vulnerability report, and strings in its evidence, that reviewers tend to question.

This is a locator for human review, not a gate. It never edits files and never
declares a report ready. Every finding is a prompt: a severity word may be
quoted from a policy, a modal verb may already carry its condition in the
previous sentence, and a path may be a documented example. Zero findings say
nothing about whether the claims were verified, which only the reporter knows.

Report checks (prose outside fenced code and inline code): em dashes, emoji and
decorative symbols, bold, hype, generated filler, courtesy and urgency padding,
severity words and a missing CVSS vector, unconditioned modal verbs in an Impact
section, scope words, vague versions, placeholders (also across a line break),
Markdown in a plain-text venue, and a missing tested-version statement.

Leak checks (report and every evidence file, including code blocks and archive
members): home directory paths, host names, private IP addresses, and
token-like strings. Every token match is masked before any output is built, so
excerpts of other findings and --json carry the masked form too.

Evidence scanning reads plain files, UTF-16 and UTF-32 files with a byte-order
mark, and .zip, .gz, .tar, .tar.gz and .tgz archives, including archives nested
up to MAX_ARCHIVE_DEPTH levels. It reads at most MAX_SCAN_BYTES of each file or
member. Hidden entries inside an evidence directory, binary files, and
unsupported archive formats are skipped; a file or member that cannot be read
becomes a scan-error finding and the run continues. The output ends with a
coverage summary that lists each file with its status, so a clean run is not
mistaken for full coverage.

Evidence checks: attachments whose names the report never mentions, and, with
--hash, a SHA-256 manifest of every evidence file.

Requires Python 3.9 or newer and only the standard library. Exit status is 0
when the run completes, whatever it finds, scan errors included, and 2 when it
cannot start: a usage error, a missing or unreadable report, a missing evidence
path, or an older Python.

The file stays whole although it is past the pack's ~500-line split point. The
skill runs it as `python3 -I`, and isolated mode removes the script's directory
from sys.path, so a sibling module such as leaks.py could not be imported.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import re
import sys
import tarfile
import zipfile
import zlib
from collections import Counter
from collections.abc import Callable, Iterator
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import BinaryIO

# Checked before any module-level code that needs 3.9 runs, so an older interpreter
# gets one line instead of a traceback.
if sys.version_info < (3, 9):
    sys.stderr.write(
        f"check_report.py needs Python 3.9 or newer; this is {sys.version_info[0]}.{sys.version_info[1]}\n"
    )
    sys.exit(2)

MAX_EXCERPT: int = 100
MAX_SHOWN_VALUE: int = 60
MAX_SCAN_BYTES: int = 20_000_000
HEADER_BYTES: int = 512
BINARY_SNIFF_BYTES: int = 8192
HASH_CHUNK_BYTES: int = 1 << 20
MAX_ARCHIVE_DEPTH: int = 3
MAX_LISTED_UNREFERENCED: int = 8
MAX_LISTED_LINES: int = 10
MAX_LISTED_SCANNED: int = 50
MAX_LISTED_VALUES: int = 3
ZIP_ENCRYPTED_FLAG: int = 0x1


class Category(str, Enum):
    """Finding categories; the values appear in output and in style-rules.md."""

    EM_DASH = "em-dash"
    EMOJI = "emoji"
    BOLD = "bold"
    HYPE = "hype"
    AI_FILLER = "ai-filler"
    COURTESY = "courtesy"
    SEVERITY_WORD = "severity-word"
    SEVERITY_NO_VECTOR = "severity-no-vector"
    IMPACT_MODAL = "impact-modal"
    SCOPE_WORD = "scope-word"
    VAGUE_VERSION = "vague-version"
    TESTED_VERSION_MISSING = "tested-version-missing"
    PLACEHOLDER = "placeholder"
    MARKDOWN_IN_PLAIN = "markdown-in-plain-text"
    PRIVATE_PATH = "private-path"
    HOSTNAME = "hostname"
    PRIVATE_IP = "private-ip"
    TOKEN = "token"
    ATTACHMENT_UNREFERENCED = "attachment-unreferenced"
    SCAN_ERROR = "scan-error"

    # (str, Enum) instead of StrEnum keeps Python 3.9 supported; this makes str() and
    # f-strings print the value on every version, as StrEnum would.
    def __str__(self) -> str:
        return self.value


class Venue(str, Enum):
    """Where the report is going; it changes which formatting is flagged."""

    PVR = "pvr"
    GHSA = "ghsa"
    H1 = "h1"
    EMAIL = "email"
    PLAIN = "plain"
    OSS_SECURITY = "oss-security"
    WRITEUP = "writeup"

    def __str__(self) -> str:
        return self.value


class ScanStatus(str, Enum):
    """What happened to one file or archive member in the coverage summary."""

    SCANNED = "scanned"
    PARTIAL = "partial"
    SKIPPED = "skipped"
    ERROR = "error"

    def __str__(self) -> str:
        return self.value


# Plain-text venues flag Markdown syntax and accept the ASCII " -- " dash idiom.
PLAIN_TEXT_VENUES: frozenset[Venue] = frozenset({Venue.EMAIL, Venue.PLAIN, Venue.OSS_SECURITY})
# These forms carry the CVSS vector in a field of its own, so a body without one is normal.
VECTOR_FIELD_VENUES: frozenset[Venue] = frozenset({Venue.H1, Venue.PVR, Venue.GHSA})


# Stdlib dataclasses instead of Pydantic models: this bundled tool must run with no
# third-party dependency on whatever Python the user has.
@dataclass(frozen=True)
class Finding:
    """One location that deserves a second look."""

    source: str
    line: int
    category: Category
    message: str
    excerpt: str


@dataclass(frozen=True)
class HashEntry:
    """SHA-256 and size of one evidence file; error is set and sha256 empty when it could not be read."""

    path: str
    sha256: str
    size: int
    error: str


@dataclass(frozen=True)
class Coverage:
    """Scan status of one report, evidence file, or archive member, with the reason when not scanned."""

    path: str
    status: ScanStatus
    detail: str


@dataclass(frozen=True)
class ScanItem:
    """A coverage record and the decoded text when the file was scanned."""

    coverage: Coverage
    text: str | None


@dataclass(frozen=True)
class Paragraph:
    """Consecutive prose lines under one heading, with the first line number."""

    first_line: int
    section: str
    text: str


# ASCII-only word boundaries. Python's \b and \w are Unicode-aware, so Hangul glued
# to an English word ("Critical로", "TODO입니다") would otherwise hide the word.
WORD_BEFORE: str = r"(?<![A-Za-z0-9_-])"
WORD_AFTER: str = r"(?![A-Za-z0-9_-])"


def _words(*phrases: str) -> re.Pattern[str]:
    """Compile whole-word, case-insensitive alternatives; a space matches any run of whitespace."""
    body: str = "|".join(re.escape(p).replace(r"\ ", r"\s+") for p in phrases)
    return re.compile(rf"{WORD_BEFORE}(?:{body}){WORD_AFTER}", re.IGNORECASE)


HYPE_RE: re.Pattern[str] = _words(
    "devastating", "catastrophic", "complete takeover", "full takeover", "total compromise",
    "complete compromise", "trivially exploitable", "trivial to exploit", "wormable", "massive",
    "extremely dangerous", "highly dangerous", "alarming", "nightmare", "unprecedented",
    "game-changing", "serious threat", "grave",
)
# Phrases only: single words such as "leverage" or "robust" are ordinary in security prose
# and in fixed advisory formulas.
AI_FILLER_RE: re.Pattern[str] = _words(
    "it is important to note", "it's important to note", "it is worth noting", "it's worth noting",
    "in summary", "in conclusion", "to summarize", "plays a crucial role", "plays a vital role",
    "plays a key role", "a testament to", "as an ai", "certainly!", "great question",
)
# "Thank you for your time" and "thanks in advance" are left out: one short thanks is fine.
COURTESY_RE: re.Pattern[str] = _words(
    "i hope this helps", "i hope this email finds you", "i hope this message finds you",
    "please do not hesitate", "please don't hesitate", "feel free to", "kindly", "dear team",
    "dear maintainers", "dear sir", "please note", "i'm happy to", "i am happy to",
    "i would be happy to", "i'd be happy to", "looking forward", "urgent", "urgently", "asap",
    "as soon as possible",
)
SEVERITY_RE: re.Pattern[str] = re.compile(
    WORD_BEFORE
    + r"(?:critical(?!\s+(?:section|path|region))|severe|high[- ](?:severity|risk|impact)"
    r"|medium[- ](?:severity|risk)|moderate[- ]severity|low[- ](?:severity|risk)"
    r"|severity\s*[:=]\s*(?:critical|high|medium|moderate|low))"
    + WORD_AFTER,
    re.IGNORECASE,
)
CVSS_MENTION_RE: re.Pattern[str] = re.compile(r"(?<![A-Za-z0-9_])CVSS(?![A-Za-z0-9_])", re.IGNORECASE)
CVSS_VECTOR_RE: re.Pattern[str] = re.compile(r"CVSS:[234]\.\d/AV:[NALP]|\bAV:[NALP]/AC:[LH]/")
MODAL_RE: re.Pattern[str] = _words(
    "could", "may", "might", "potentially", "possibly", "conceivably", "theoretically",
)
# "under", "where", and "only" are left out: "files under /etc" and "where possible"
# bound nothing, so they must not excuse a modal claim.
CONDITION_RE: re.Pattern[str] = _words(
    "if", "when", "whenever", "unless", "provided", "given", "assuming", "as long as", "once",
    "requires", "require", "required", "requiring", "depends", "depending", "in deployments",
    "in configurations",
)
SCOPE_RE: re.Pattern[str] = _words(
    "every version", "any version", "all users", "every user", "any user", "all deployments",
    "every deployment", "any deployment", "any attacker", "all instances",
)
VAGUE_VERSION_RE: re.Pattern[str] = re.compile(
    WORD_BEFORE
    + r"(?:all\s+versions|latest\s+(?:version|release|master|main|mainline|commit|build)"
    r"|current\s+(?:version|release|master|main)|newest\s+version|recent\s+versions?)"
    + WORD_AFTER,
    re.IGNORECASE,
)
# A hex run with at least one digit and one letter, so ordinary words are not commits.
COMMIT_RE: re.Pattern[str] = re.compile(
    r"(?<![A-Za-z0-9])(?=[0-9a-f]{0,39}[0-9])(?=[0-9a-f]{0,39}[a-f])[0-9a-f]{7,40}(?![A-Za-z0-9])",
)
PLACEHOLDER_OPEN: str = (
    r"<(?!https?://|mailto:|/?(?:br|p|div|span|details|summary|sup|sub|kbd|img|a)\b|[^<>]*@)[A-Za-z]"
)
PLACEHOLDER_RE: re.Pattern[str] = re.compile(
    r"(?<![A-Za-z0-9_])(?:TODO|TBD|FIXME|XXX|DRAFT)(?![A-Za-z0-9_])|<!--|\{\{[^}]*\}\}"
    r"|\[placeholder\]|lorem ipsum|" + PLACEHOLDER_OPEN + r"[^<>\n]{1,60}>",
)
# A template placeholder wrapped over two to five non-blank lines, as in the plain-text assets.
MULTILINE_PLACEHOLDER_RE: re.Pattern[str] = re.compile(
    PLACEHOLDER_OPEN + r"[^<>\n]*(?:\n[ \t]*[^<>\s][^<>\n]*){1,4}>",
)
EM_DASH_RE: re.Pattern[str] = re.compile(r"[—―]|\s–\s|\s--\s")
PLAIN_EM_DASH_RE: re.Pattern[str] = re.compile(r"[—―]|\s–\s")
EMOJI_RE: re.Pattern[str] = re.compile(
    "[\U0001F000-\U0001FAFF☀-➿⭐⭕‼⁉️→⇒➜]",
)
# Underscore emphasis counts only when it holds a space, so identifiers such as
# __init__ and __proto__ written outside backticks are not taken for bold.
BOLD_RE: re.Pattern[str] = re.compile(r"\*\*[^*\n]+?\*\*|(?<!\w)__(?=[^_\n]*\s)[^_\n]+?__(?!\w)")
BOLD_LABEL_LINE_RE: re.Pattern[str] = re.compile(r"^\s*(?:[-*]\s+)?\*\*[^*\n]{1,40}?:?\*\*:?\s*")
MARKDOWN_RE: re.Pattern[str] = re.compile(
    r"^\s{0,3}#{1,6}\s|\*\*[^*\n]+\*\*|\[[^\]\n]+\]\([^)\n]+\)|^\s*\|.*\|\s*$|^\s*(?:```|~~~)",
)
FENCE_RE: re.Pattern[str] = re.compile(r"^\s*(?:```|~~~)")
INDENTED_CODE_RE: re.Pattern[str] = re.compile(r"^(?: {4,}|\t)(?![-*+]\s|\d+[.)]\s)\S")
INLINE_CODE_RE: re.Pattern[str] = re.compile(r"`[^`\n]*`")
URL_RE: re.Pattern[str] = re.compile(r"https?://\S+")
HTML_COMMENT_RE: re.Pattern[str] = re.compile(r"<!--.*?-->")
CURLY_APOSTROPHES: dict[int, str] = str.maketrans({"‘": "'", "’": "'"})
MD_HEADING_RE: re.Pattern[str] = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
LABEL_HEADING_RE: re.Pattern[str] = re.compile(
    r"^\s*(?:\*\*)?([A-Z][A-Za-z0-9 /&()'-]{1,50}?):?(?:\*\*)?:?\s*$",
)
# "Impact: text" on one line opens an Impact paragraph, as a heading would.
INLINE_IMPACT_LABEL_RE: re.Pattern[str] = re.compile(
    r"^\s*(?:[-*]\s+)?(?:\*\*|__)?(?P<label>impact|consequences?|risks?)(?:\*\*|__)?\s*:\s*(?:\*\*|__)?\s*\S",
    re.IGNORECASE,
)
SETEXT_RE: re.Pattern[str] = re.compile(r"^\s*(?:=+|-+)\s*$")
SENTENCE_SPLIT_RE: re.Pattern[str] = re.compile(r"(?<=[.!?])\s+")
IMPACT_SECTION_RE: re.Pattern[str] = re.compile(r"impact|consequence|risk", re.IGNORECASE)
NOT_IMPACT_SECTION_RE: re.Pattern[str] = re.compile(r"not affected|unaffected", re.IGNORECASE)

# "Affected versions" is a range, not a tested version, so it does not count here.
TESTED_HEADING_RE: re.Pattern[str] = re.compile(
    r"^\s*(?:#{1,6}\s*)?(?:[-*]\s+)?(?:\*\*)?\s*(?:tested\s+(?:version|on|against|with)"
    r"|versions?\s+tested|checked\s+on|reproduction\s+environment|environment|platform|version)\b",
    re.IGNORECASE | re.MULTILINE,
)
# Scoring systems and protocols carry version numbers too ("using CVSS 3.1", "over TLS 1.3").
STANDARD_NAMES: str = r"CVSS|CWE|CVE|RFC|ISO|OWASP|TLS|SSL|HTTPS?|SSH|OAuth|SAML|UTF"
KOREAN_TESTED_WORDS: str = r"버전|테스트|재현|확인|검증"
TESTED_SENTENCE_RE: re.Pattern[str] = re.compile(
    r"\b(?:tested|reproduced|verified|confirmed|observed|ran|executed|checked)\b[^.\n]{0,100}?"
    r"(?:\bv?\d+\.\d+(?:\.\d+)?\b|\b[0-9a-f]{7,40}\b)"
    r"|\bversion\s*[:=]?\s*v?\d+\.\d+"
    rf"|\b(?:in|on|against|with|using)\s+(?!(?:{STANDARD_NAMES})\b)"
    r"(?:(?-i:[A-Z])[\w.+-]*\s+){1,3}v?\d+\.\d+(?:\.\d+)?\b"
    rf"|(?:{KOREAN_TESTED_WORDS})[^.\n]{{0,40}}?\d+\.\d+"
    rf"|\d+\.\d+(?:\.\d+)?[^.\n]{{0,40}}?(?:{KOREAN_TESTED_WORDS})",
    re.IGNORECASE,
)

PRIVATE_PATH_RE: re.Pattern[str] = re.compile(
    r"/Users/[A-Za-z0-9._-]+|/home/[A-Za-z0-9._-]+|[A-Za-z]:\\Users\\[^\\\s\"']+"
    r"|/private/var/folders/\S+|/var/folders/[\w]{2}/\S+",
)
# In evidence, generic home references also matter: a log that prints $HOME or ~/ was
# usually captured on someone's machine. In report prose they are ordinary notation.
EVIDENCE_PATH_RE: re.Pattern[str] = re.compile(
    PRIVATE_PATH_RE.pattern + r"|\$HOME\b|%USERPROFILE%|(?<![\w/.~])~/[\w.-]+",
)
# Three host shapes. (1) A name under an internal suffix, not preceded by a single "/"
# (a path such as /sbin/kadmin.local) and not followed by "(" or another label (a Python
# attribute such as threading.local() or a file such as settings.local.json). (2) An
# owner-prefixed machine name such as alice-macbook-pro, any case. (3) user@host in a
# shell-prompt position or at the end of a line, excluding version, digest, and tag pins
# such as checkout@v4, action@<sha>, image@sha256, and pkg@latest.
INTERNAL_SUFFIXES: str = r"local|lan|internal|intranet|corp|localdomain|home\.arpa|ts\.net"
MACHINE_WORDS: str = r"macbook|mbp|imac|mac-?mini|mac-?studio|laptop"
PIN_TAGS: str = r"latest|next|main|master|stable|beta|alpha|canary|nightly|edge|head"
HOSTNAME_RE: re.Pattern[str] = re.compile(
    r"(?:(?<=//)|(?<![A-Za-z0-9_./\\-]))(?!localhost\.localdomain\b)"
    rf"[A-Za-z0-9][A-Za-z0-9-]{{0,62}}(?:\.[A-Za-z0-9-]{{1,63}})*\.(?:{INTERNAL_SUFFIXES})"
    r"(?![A-Za-z0-9_(-]|\.[A-Za-z0-9])"
    rf"|(?i:(?<![A-Za-z0-9_.-])(?:[A-Za-z0-9]+-)+(?:{MACHINE_WORDS})(?:-[A-Za-z0-9]+)*(?![A-Za-z0-9_-]))"
    r"|(?<![A-Za-z0-9_.@/-])[a-z_][a-z0-9_-]{0,31}@"
    rf"(?!v\d|sha\d|(?:{PIN_TAGS})(?![A-Za-z0-9-])|[0-9a-f]{{7,}}(?![A-Za-z0-9-]))"
    r"[A-Za-z][A-Za-z0-9-]{0,62}(?=:[~/]|\s*[$#%>\]]|\s+[~/]|\s*$)",
)
PRIVATE_IP_RE: re.Pattern[str] = re.compile(
    r"(?<![\d.])(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}"
    r"|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}"
    r"|100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.\d{1,3}\.\d{1,3})(?!\d|\.\d)",
)
# Three token shapes, told apart by group name so masking can keep a label readable.
# "known": a vendor prefix or structure (ghp_, sk-, AKIA, JWT, PEM header).
# "bearer": an Authorization bearer value of 20 or more characters.
# "key": a value assigned to a secret-like key name, prefixed or not (APP_API_KEY=,
# DB_PASSWORD=, "access_token": ); the value needs 6 characters with a digit or 12 without.
SECRET_KEY_NAMES: str = (
    r"api[_-]?key|access[_-]?key|secret[_-]?key|private[_-]?key|client[_-]?secret"
    r"|secret|token|password|passwd|passphrase"
)
SECRET_VALUE: str = r"[A-Za-z0-9_.~+/=-]"
TOKEN_RE: re.Pattern[str] = re.compile(
    r"(?P<known>(?<![A-Za-z0-9_])(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{22,}"
    r"|sk-(?:ant-|proj-)?[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}"
    r"|xox[abprs]-[A-Za-z0-9-]{10,}|hf_[A-Za-z0-9]{30,}|npm_[A-Za-z0-9]{36}"
    r"|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})(?![A-Za-z0-9])"
    r"|-----BEGIN [A-Z ]*PRIVATE KEY-----)"
    rf"|(?P<bearer>(?<![A-Za-z0-9_])(?i:bearer)\s+)(?P<bearer_value>{SECRET_VALUE}{{20,}})"
    rf"|(?P<key>(?<![A-Za-z0-9])(?i:[A-Za-z0-9_]*?(?:{SECRET_KEY_NAMES}))[\"']?\s*[:=]\s*[\"']?)"
    rf"(?P<key_value>(?={SECRET_VALUE}*\d){SECRET_VALUE}{{6,}}|{SECRET_VALUE}{{12,}})",
)

# Lowercase literals every TOKEN_RE match contains. A line with none of them skips TOKEN_RE,
# whose lookbehinds and lazy key-name prefix cost far more per line than substring tests.
TOKEN_HINTS: tuple[str, ...] = (
    "key", "secret", "token", "passw", "passphrase", "bearer", "ghp_", "gho_", "ghu_", "ghs_", "ghr_",
    "github_pat_", "sk-", "akia", "aiza", "xox", "hf_", "npm_", "eyj", "-----begin",
)

# A plain alias rather than a `type` statement keeps Python 3.9 supported.
LeakCheck = tuple[Category, re.Pattern[str], str]

REPORT_LEAK_CHECKS: tuple[LeakCheck, ...] = (
    (Category.PRIVATE_PATH, PRIVATE_PATH_RE, "Home directory or user-specific path"),
    (Category.HOSTNAME, HOSTNAME_RE, "Host name or user@host prompt"),
    (Category.PRIVATE_IP, PRIVATE_IP_RE, "Private or carrier-grade NAT address"),
    (Category.TOKEN, TOKEN_RE, "Token-like or secret-like string (value masked)"),
)
EVIDENCE_LEAK_CHECKS: tuple[LeakCheck, ...] = (
    (Category.PRIVATE_PATH, EVIDENCE_PATH_RE, "Home directory, $HOME, or ~/ path"),
    *REPORT_LEAK_CHECKS[1:],
)
# Categories that repeat on many lines of a normal document. They are reported once per
# file with the other line numbers, so a long log or a bold-heavy body stays readable.
AGGREGATED: frozenset[Category] = frozenset({
    Category.BOLD, Category.EM_DASH, Category.EMOJI, Category.SCOPE_WORD,
    Category.MARKDOWN_IN_PLAIN, Category.PRIVATE_IP,
})
EVIDENCE_AGGREGATED: frozenset[Category] = frozenset(Category)

# Magic numbers of compressed formats this script does not open; reported by name.
UNSUPPORTED_ARCHIVES: tuple[tuple[bytes, str], ...] = (
    (b"BZh", "bzip2"), (b"\xfd7zXZ\x00", "xz"), (b"7z\xbc\xaf\x27\x1c", "7z"),
    (b"Rar!\x1a\x07", "rar"), (b"\x28\xb5\x2f\xfd", "zstd"),
)
# Library errors a malformed, encrypted, or unreadable file can raise while it is scanned.
# They are translated once, in _describe_error, into a scan-error finding.
SCAN_ERRORS: tuple[type[BaseException], ...] = (
    OSError, RuntimeError, EOFError, ValueError, NotImplementedError,
    zipfile.BadZipFile, tarfile.TarError, zlib.error,
)


def main(argv: list[str] | None = None) -> int:
    """Run the checks and print findings; return 0 on a completed run, 2 when it cannot start."""
    args: argparse.Namespace = _parse_args(argv)
    report_path: Path = Path(args.report)
    evidence_paths: list[Path] = [Path(p) for p in args.evidence]
    problem: str = _input_problem(report_path, evidence_paths)
    if problem:
        print(f"error: {problem}", file=sys.stderr)
        return 2
    try:
        report: ScanItem = _read_report(report_path)
    except OSError as error:
        print(f"error: cannot read report {report_path}: {_describe_error(error)}", file=sys.stderr)
        return 2

    report_text: str = report.text or ""
    venue: Venue = Venue(args.venue)
    findings: list[Finding] = check_report(report_text, str(report_path), venue)
    evidence_findings: list[Finding]
    evidence_coverage: list[Coverage]
    evidence_findings, evidence_coverage = check_evidence(evidence_paths, report_text)
    findings.extend(evidence_findings)
    coverage: list[Coverage] = [report.coverage, *evidence_coverage]
    hashes: list[HashEntry] = hash_evidence(evidence_paths) if args.hash else []

    if args.json:
        print(render_json(findings, coverage, hashes))
    else:
        print(render_text(findings, coverage, hashes))
    return 0


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Flag report passages and evidence strings for human review. Not a gate.",
    )
    parser.add_argument("report", help="report file, Markdown or plain text")
    parser.add_argument(
        "--evidence", nargs="*", default=[], metavar="PATH",
        help="evidence files or directories to scan for leaks and references; .zip, .gz, .tar,"
             " .tar.gz, and .tgz are opened, nested up to three levels; hidden entries inside a"
             " directory are skipped and listed",
    )
    parser.add_argument(
        "--venue", choices=[v.value for v in Venue], default=Venue.PVR.value,
        help="destination (default: pvr); email, plain, and oss-security flag Markdown syntax and"
             " accept ' -- '; pvr, ghsa, and h1 skip severity-no-vector because the form has a"
             " vector field",
    )
    parser.add_argument("--hash", action="store_true", help="print a SHA-256 manifest of evidence files")
    parser.add_argument("--json", action="store_true", help="print JSON instead of text")
    return parser.parse_args(argv)


def _input_problem(report: Path, evidence: list[Path]) -> str:
    """Return a one-line usage problem with the given paths, or an empty string."""
    if report.is_dir():
        return f"report is a directory, not a file: {report}"
    if not report.exists():
        return f"report not found: {report}"
    if not report.is_file():
        return f"report is not a regular file: {report}"
    missing: list[Path] = [p for p in evidence if not p.exists()]
    if missing:
        return f"evidence not found: {', '.join(str(p) for p in missing)}"
    special: list[Path] = [p for p in evidence if not (p.is_file() or p.is_dir())]
    if special:
        return f"evidence is not a regular file or directory: {', '.join(str(p) for p in special)}"
    return ""


def _read_report(path: Path) -> ScanItem:
    """Read and decode the report; raise OSError when it cannot be read."""
    with path.open("rb") as handle:
        data: bytes = handle.read(MAX_SCAN_BYTES + 1)
    item: ScanItem = _text_item(str(path), data)
    if item.text is None:
        # NUL bytes and no byte-order mark: the user named this file as the report, so read it anyway.
        text: str = data[:MAX_SCAN_BYTES].decode("utf-8", errors="replace")
        return ScanItem(Coverage(str(path), ScanStatus.SCANNED, "report; contains NUL bytes"), text)
    detail: str = "; ".join(d for d in ("report", item.coverage.detail) if d)
    return ScanItem(Coverage(item.coverage.path, item.coverage.status, detail), item.text)


def check_report(text: str, source: str, venue: Venue) -> list[Finding]:
    """Return style, claim, and leak findings for one report text, with every token masked."""
    raw_lines: list[str] = text.splitlines()
    lines: list[str] = [mask_secrets(line) for line in raw_lines]
    code_mask: list[bool] = _code_line_mask(lines)
    findings: list[Finding] = []

    for index, raw_line in enumerate(raw_lines):
        number: int = index + 1
        line: str = lines[index]
        findings.extend(_leak_findings(raw_line, source, number, REPORT_LEAK_CHECKS))
        if venue in PLAIN_TEXT_VENUES and MARKDOWN_RE.search(line):
            findings.append(_finding(source, number, Category.MARKDOWN_IN_PLAIN,
                                     "Markdown syntax in a plain-text venue", line))
        if code_mask[index]:
            continue
        findings.extend(_prose_line_findings(line, source, number, venue))

    findings.extend(_multiline_placeholder_findings(lines, code_mask, source))
    for paragraph in _paragraphs(lines, code_mask):
        findings.extend(_impact_modal_findings(paragraph, source))
    findings.extend(_document_findings(lines, code_mask, source, venue))
    return aggregate(findings, AGGREGATED)


def _code_line_mask(lines: list[str]) -> list[bool]:
    """Mark fenced and indented code lines, fences included, so prose checks skip them.

    An indented line counts as code unless it starts a nested list item, so quoted
    source and transcripts in plain-text reports are skipped as well.
    """
    mask: list[bool] = []
    inside: bool = False
    for line in lines:
        if FENCE_RE.match(line):
            mask.append(True)
            inside = not inside
            continue
        mask.append(inside or bool(INDENTED_CODE_RE.match(line)))
    return mask


def _prose(line: str) -> str:
    """Strip inline code, URLs, and HTML comments and straighten apostrophes, keeping only prose."""
    without_code: str = INLINE_CODE_RE.sub(" ", line)
    without_urls: str = URL_RE.sub(" ", without_code)
    return HTML_COMMENT_RE.sub(" ", without_urls).translate(CURLY_APOSTROPHES)


def _prose_line_findings(line: str, source: str, number: int, venue: Venue) -> list[Finding]:
    prose: str = _prose(line)
    found: list[Finding] = []
    dash: re.Pattern[str] = PLAIN_EM_DASH_RE if venue in PLAIN_TEXT_VENUES else EM_DASH_RE
    word_checks: tuple[tuple[Category, re.Pattern[str], str], ...] = (
        (Category.EM_DASH, dash, "Em dash or spaced dash as punctuation"),
        (Category.EMOJI, EMOJI_RE, "Emoji, arrow, or decorative symbol"),
        (Category.HYPE, HYPE_RE, "Hype word; state the demonstrated effect instead"),
        (Category.AI_FILLER, AI_FILLER_RE, "Generated-text filler"),
        (Category.COURTESY, COURTESY_RE, "Courtesy or urgency padding"),
        (Category.SEVERITY_WORD, SEVERITY_RE, "Severity word; is it supported, wanted by the venue, and vectored?"),
        (Category.SCOPE_WORD, SCOPE_RE, "Scope word; state what was actually checked"),
    )
    for category, pattern, message in word_checks:
        match: re.Match[str] | None = pattern.search(prose)
        if match:
            found.append(_finding(source, number, category, f"{message}: '{match.group(0).strip()}'", line))
    vague: re.Match[str] | None = VAGUE_VERSION_RE.search(prose)
    if vague and not COMMIT_RE.search(_sentence_at(prose, vague.start())):
        found.append(_finding(source, number, Category.VAGUE_VERSION,
                              f"Vague version; give the exact release or commit: '{vague.group(0)}'", line))
    placeholder: re.Match[str] | None = PLACEHOLDER_RE.search(INLINE_CODE_RE.sub(" ", line))
    if placeholder:
        found.append(_finding(source, number, Category.PLACEHOLDER,
                              f"Placeholder or template residue: '{placeholder.group(0)}'", line))
    found.extend(_bold_findings(prose, line, source, number, venue))
    return found


def _sentence_at(text: str, position: int) -> str:
    """Return the sentence of text that contains position."""
    start: int = 0
    for boundary in SENTENCE_SPLIT_RE.finditer(text):
        if boundary.start() >= position:
            return text[start:boundary.start()]
        start = boundary.end()
    return text[start:]


def _bold_findings(prose: str, line: str, source: str, number: int, venue: Venue) -> list[Finding]:
    if not BOLD_RE.search(prose):
        return []
    label: re.Match[str] | None = BOLD_LABEL_LINE_RE.match(prose)
    if label and venue is Venue.H1 and not BOLD_RE.search(prose[label.end():]):
        return []
    if label:
        message: str = "Bold label used as a pseudo-heading; prefer a heading or plain label"
    else:
        message = "Bold inside prose"
    return [_finding(source, number, Category.BOLD, message, line)]


def _multiline_placeholder_findings(lines: list[str], code_mask: list[bool], source: str) -> list[Finding]:
    """Flag <...> placeholders wrapped across lines, which the per-line check cannot see."""
    prose_lines: list[str] = ["" if code_mask[i] else INLINE_CODE_RE.sub(" ", line) for i, line in enumerate(lines)]
    document: str = "\n".join(prose_lines)
    found: list[Finding] = []
    for match in MULTILINE_PLACEHOLDER_RE.finditer(document):
        number: int = document.count("\n", 0, match.start()) + 1
        shown: str = _shorten(" ".join(match.group(0).split()), MAX_SHOWN_VALUE)
        found.append(_finding(source, number, Category.PLACEHOLDER,
                              f"Placeholder spanning lines: '{shown}'", lines[number - 1]))
    return found


def _paragraphs(lines: list[str], code_mask: list[bool]) -> Iterator[Paragraph]:
    """Yield prose paragraphs with the heading they sit under.

    A line that opens with an inline "Impact:" label starts a paragraph of its own whose
    section is that label; the next paragraph returns to the enclosing heading.
    """
    section: str = ""
    paragraph_section: str = ""
    buffer: list[str] = []
    first_line: int = 0
    for index, line in enumerate(lines):
        heading: str | None = _heading_text(lines, index)
        skipped: bool = code_mask[index] or not line.strip() or heading is not None
        inline: re.Match[str] | None = None if skipped else INLINE_IMPACT_LABEL_RE.match(line)
        if (skipped or inline) and buffer:
            yield Paragraph(first_line, paragraph_section, " ".join(buffer))
            buffer = []
        if heading is not None:
            section = heading
        if skipped or SETEXT_RE.match(line):
            continue
        if not buffer:
            first_line = index + 1
            paragraph_section = inline.group("label") if inline else section
        buffer.append(_prose(line).strip())
    if buffer:
        yield Paragraph(first_line, paragraph_section, " ".join(buffer))


def _heading_text(lines: list[str], index: int) -> str | None:
    """Return the heading text if this line is a Markdown, setext, or label heading."""
    line: str = lines[index]
    markdown: re.Match[str] | None = MD_HEADING_RE.match(line)
    if markdown:
        return markdown.group(1).strip("*_ ")
    following: str = lines[index + 1] if index + 1 < len(lines) else ""
    if line.strip() and SETEXT_RE.match(following) and len(following.strip()) >= 3:
        return line.strip()
    label: re.Match[str] | None = LABEL_HEADING_RE.match(line)
    if label and len(line.strip()) <= 60:
        return label.group(1).strip()
    return None


def _impact_modal_findings(paragraph: Paragraph, source: str) -> list[Finding]:
    """Flag modal claims in an Impact section that carry no condition in the same sentence."""
    if not IMPACT_SECTION_RE.search(paragraph.section) or NOT_IMPACT_SECTION_RE.search(paragraph.section):
        return []
    found: list[Finding] = []
    for sentence in SENTENCE_SPLIT_RE.split(paragraph.text):
        modal: re.Match[str] | None = MODAL_RE.search(sentence)
        if modal and not CONDITION_RE.search(sentence):
            found.append(_finding(
                source, paragraph.first_line, Category.IMPACT_MODAL,
                f"'{modal.group(0)}' in the Impact paragraph starting here, with no condition in the same sentence;"
                " demonstrate it or state the condition",
                sentence,
            ))
    return found


def _document_findings(lines: list[str], code_mask: list[bool], source: str, venue: Venue) -> list[Finding]:
    """Checks that need the whole document: tested version and CVSS vector."""
    document: str = "\n".join(lines)
    found: list[Finding] = []
    if not TESTED_HEADING_RE.search(document) and not TESTED_SENTENCE_RE.search(document):
        found.append(_finding(source, 1, Category.TESTED_VERSION_MISSING,
                              "No tested-version statement found; name the release or commit you ran",
                              lines[0] if lines else ""))
    if venue in VECTOR_FIELD_VENUES or CVSS_VECTOR_RE.search(document):
        return found
    for index, line in enumerate(lines):
        if code_mask[index]:
            continue
        prose: str = _prose(line)
        if CVSS_MENTION_RE.search(prose) or SEVERITY_RE.search(prose):
            found.append(_finding(source, index + 1, Category.SEVERITY_NO_VECTOR,
                                  "Severity or CVSS appears but no CVSS vector does anywhere in the report", line))
            break
    return found


def _leak_findings(line: str, source: str, number: int, checks: tuple[LeakCheck, ...]) -> list[Finding]:
    """Leak findings for one raw line; values are taken from the masked line, so no token is shown."""
    safe: str = mask_secrets(line)
    found: list[Finding] = []
    for category, pattern, message in checks:
        if category is Category.TOKEN:
            values: list[str] = [_masked(m) for m in pattern.finditer(line)] if _may_hold_token(line) else []
        else:
            values = [m.group(0) for m in pattern.finditer(safe)]
        if not values:
            continue
        distinct: list[str] = list(dict.fromkeys(values))
        shown: str = ", ".join(f"'{v}'" for v in distinct[:MAX_LISTED_VALUES])
        if len(distinct) > MAX_LISTED_VALUES:
            shown += f", and {len(distinct) - MAX_LISTED_VALUES} more"
        found.append(_finding(source, number, category, f"{message}: {shown}", safe))
    return found


def mask_secrets(text: str) -> str:
    """Replace every token-like match in text with its masked form.

    Masked forms do not match TOKEN_RE again, so masking twice changes nothing.
    """
    return TOKEN_RE.sub(_masked, text) if _may_hold_token(text) else text


def _may_hold_token(text: str) -> bool:
    lowered: str = text.lower()
    return any(hint in lowered for hint in TOKEN_HINTS)


def _masked(match: re.Match[str]) -> str:
    """Known formats keep their 4-character prefix; labeled values keep the label and lose every character."""
    known: str | None = match.group("known")
    if known:
        return f"{known[:4]}...[{len(known)} chars]"
    label: str = match.group("bearer") or match.group("key")
    value: str = match.group("bearer_value") or match.group("key_value")
    return f"{label}[masked, {len(value)} chars]"


def check_evidence(paths: list[Path], report_text: str) -> tuple[list[Finding], list[Coverage]]:
    """Scan evidence for leaks, list unnamed attachments, and record what was and was not scanned."""
    findings: list[Finding] = []
    coverage: list[Coverage] = []
    for path in paths:
        files: list[Path]
        left_out: list[Coverage]
        files, left_out = _walk(path)
        items: list[ScanItem] = [ScanItem(record, None) for record in left_out]
        for file in files:
            items.extend(_file_items(file))
        for item in items:
            coverage.append(item.coverage)
            if item.coverage.status is ScanStatus.ERROR:
                findings.append(_finding(item.coverage.path, 0, Category.SCAN_ERROR,
                                         f"Not scanned: {item.coverage.detail}", ""))
            if item.text is not None:
                findings.extend(_text_leak_findings(item.coverage.path, item.text))
        findings.extend(_unreferenced(path, report_text))
    return findings, coverage


def _text_leak_findings(label: str, text: str) -> list[Finding]:
    leaks: list[Finding] = []
    for index, line in enumerate(text.splitlines()):
        leaks.extend(_leak_findings(line, label, index + 1, EVIDENCE_LEAK_CHECKS))
    return aggregate(leaks, EVIDENCE_AGGREGATED)


def _walk(path: Path) -> tuple[list[Path], list[Coverage]]:
    """Return the regular files under an evidence argument and coverage records for entries left out.

    A file argument is returned as is, hidden or not, because the user named it. Inside a
    directory, hidden files and directories (.git, .DS_Store, .env) are left out of the scan,
    the reference check, and the manifest, and reported as skipped; unreadable directories
    are reported as errors.
    """
    if not path.is_dir():
        return [path], []
    files: list[Path] = []
    left_out: list[Coverage] = []

    def on_error(error: OSError) -> None:
        left_out.append(Coverage(str(error.filename), ScanStatus.ERROR, _describe_error(error)))

    for directory, dirnames, filenames in os.walk(path, onerror=on_error):
        base: Path = Path(directory)
        for name in sorted(dirnames):
            entry: Path = base / name
            if name.startswith("."):
                left_out.append(Coverage(str(entry), ScanStatus.SKIPPED, "hidden directory"))
            elif entry.is_symlink():
                left_out.append(Coverage(str(entry), ScanStatus.SKIPPED, "symbolic link to a directory"))
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        for name in sorted(filenames):
            entry = base / name
            if name.startswith("."):
                left_out.append(Coverage(str(entry), ScanStatus.SKIPPED, "hidden file"))
            elif not entry.is_file():
                left_out.append(Coverage(str(entry), ScanStatus.SKIPPED, "not a regular file"))
            else:
                files.append(entry)
    return sorted(files), left_out


def _file_items(file: Path) -> Iterator[ScanItem]:
    try:
        handle: BinaryIO = file.open("rb")
    except OSError as error:
        yield _error_item(str(file), error)
        return
    with handle:
        yield from _blob_items(str(file), handle, 0)


def _blob_items(label: str, handle: BinaryIO, depth: int) -> Iterator[ScanItem]:
    """Yield scan items for one seekable file or member; depth counts the archives around it."""
    try:
        head: bytes = handle.read(HEADER_BYTES)
        handle.seek(0)
        kind: str = _archive_kind(head)
        data: bytes = handle.read(MAX_SCAN_BYTES + 1) if not kind else b""
    except SCAN_ERRORS as error:
        yield _error_item(label, error)
        return
    if not kind:
        yield _text_item(label, data)
        return
    if kind not in ("zip", "gzip", "tar"):
        yield ScanItem(Coverage(label, ScanStatus.SKIPPED, f"{kind} archive, not opened by this script"), None)
        return
    if depth >= MAX_ARCHIVE_DEPTH:
        yield ScanItem(Coverage(label, ScanStatus.SKIPPED,
                                f"{kind} archive nested deeper than {MAX_ARCHIVE_DEPTH} levels"), None)
        return
    readers: dict[str, Callable[[str, BinaryIO, int], Iterator[ScanItem]]] = {
        "zip": _zip_items, "tar": _tar_items, "gzip": _gzip_items,
    }
    members: int = 0
    try:
        for item in readers[kind](label, handle, depth + 1):
            members += 1
            yield item
    except SCAN_ERRORS as error:
        yield _error_item(label, error)
        return
    if not members:
        yield ScanItem(Coverage(label, ScanStatus.SKIPPED, f"empty {kind} archive"), None)


def _archive_kind(head: bytes) -> str:
    """Name the archive format from the first bytes, or return an empty string for other files."""
    if head.startswith((b"PK\x03\x04", b"PK\x05\x06")):
        return "zip"
    if head.startswith(b"\x1f\x8b"):
        return "gzip"
    if head[257:262] == b"ustar":
        return "tar"
    for magic, name in UNSUPPORTED_ARCHIVES:
        if head.startswith(magic):
            return name
    return ""


def _zip_items(label: str, handle: BinaryIO, depth: int) -> Iterator[ScanItem]:
    with zipfile.ZipFile(handle) as bundle:
        for info in bundle.infolist():
            if info.is_dir():
                continue
            member: str = f"{label}!{info.filename}"
            if info.flag_bits & ZIP_ENCRYPTED_FLAG:
                yield ScanItem(Coverage(member, ScanStatus.ERROR, "encrypted, password required"), None)
                continue
            try:
                with bundle.open(info) as stream:
                    data: bytes = stream.read(MAX_SCAN_BYTES + 1)
            except SCAN_ERRORS as error:
                yield _error_item(member, error)
                continue
            yield from _blob_items(member, io.BytesIO(data), depth)


def _tar_items(label: str, handle: BinaryIO, depth: int) -> Iterator[ScanItem]:
    # Members are read into memory, never extracted to disk, so member paths cannot escape.
    with tarfile.open(fileobj=handle, mode="r:*") as bundle:
        for info in bundle:
            if info.isdir():
                continue
            member: str = f"{label}!{info.name}"
            if not info.isfile():
                yield ScanItem(Coverage(member, ScanStatus.SKIPPED, "not a regular file"), None)
                continue
            try:
                stream: BinaryIO | None = bundle.extractfile(info)
                data: bytes = stream.read(MAX_SCAN_BYTES + 1) if stream else b""
            except SCAN_ERRORS as error:
                yield _error_item(member, error)
                continue
            yield from _blob_items(member, io.BytesIO(data), depth)


def _gzip_items(label: str, handle: BinaryIO, depth: int) -> Iterator[ScanItem]:
    """A .tar.gz streams through tarfile; any other .gz is one member, the decompressed file."""
    with gzip.GzipFile(fileobj=handle) as stream:
        head: bytes = stream.read(HEADER_BYTES)
    handle.seek(0)
    if head[257:262] == b"ustar":
        yield from _tar_items(label, handle, depth)
        return
    with gzip.GzipFile(fileobj=handle) as stream:
        data: bytes = stream.read(MAX_SCAN_BYTES + 1)
    inner: str = Path(label.rsplit("!", 1)[-1]).stem
    yield from _blob_items(f"{label}!{inner}", io.BytesIO(data), depth)


def _text_item(label: str, data: bytes) -> ScanItem:
    """Decode up to MAX_SCAN_BYTES of data, or mark it binary."""
    truncated: bool = len(data) > MAX_SCAN_BYTES
    decoded: tuple[str, str] | None = _decode(data[:MAX_SCAN_BYTES])
    if decoded is None:
        return ScanItem(Coverage(label, ScanStatus.SKIPPED, "binary"), None)
    text: str
    note: str
    text, note = decoded
    notes: list[str] = [n for n in (note, f"first {MAX_SCAN_BYTES} bytes only" if truncated else "") if n]
    status: ScanStatus = ScanStatus.PARTIAL if truncated else ScanStatus.SCANNED
    return ScanItem(Coverage(label, status, "; ".join(notes)), text)


def _decode(data: bytes) -> tuple[str, str] | None:
    """Return (text, note) for text data, or None for binary; the note names a non-UTF-8 decoding."""
    if not data:
        return "", "empty"
    boms: tuple[tuple[bytes, str], ...] = (
        (b"\xff\xfe\x00\x00", "utf-32"), (b"\x00\x00\xfe\xff", "utf-32"),
        (b"\xff\xfe", "utf-16"), (b"\xfe\xff", "utf-16"), (b"\xef\xbb\xbf", "utf-8-sig"),
    )
    for bom, encoding in boms:
        if data.startswith(bom):
            note: str = "" if encoding == "utf-8-sig" else encoding
            return data.decode(encoding, errors="replace"), note
    if b"\x00" in data[:BINARY_SNIFF_BYTES]:
        return None
    try:
        return data.decode("utf-8"), ""
    except UnicodeDecodeError:
        return data.decode("utf-8", errors="replace"), "not valid UTF-8; bad bytes replaced"


def _error_item(label: str, error: BaseException) -> ScanItem:
    return ScanItem(Coverage(label, ScanStatus.ERROR, _describe_error(error)), None)


def _describe_error(error: BaseException) -> str:
    """Translate a library error raised while reading evidence into a short reason."""
    if isinstance(error, PermissionError):
        return "permission denied"
    if isinstance(error, RuntimeError) and "encrypted" in str(error):
        return "encrypted, password required"
    if isinstance(error, zipfile.BadZipFile):
        return f"corrupt zip: {error}"
    if isinstance(error, tarfile.TarError):
        return f"corrupt tar: {error}"
    if isinstance(error, gzip.BadGzipFile):
        return f"corrupt gzip: {error}"
    if isinstance(error, (EOFError, zlib.error)):
        return f"truncated or corrupt compressed data: {error}"
    if isinstance(error, NotImplementedError):
        return f"unsupported compression: {error}"
    if isinstance(error, OSError) and error.strerror:
        return error.strerror
    return f"{type(error).__name__}: {error}"


def _unreferenced(path: Path, report_text: str) -> list[Finding]:
    """One finding per evidence argument whose files the report does not name as a whole token."""
    if path.is_file():
        if _names(report_text, path.name):
            return []
        return [_finding(str(path), 0, Category.ATTACHMENT_UNREFERENCED,
                         f"The report never names '{path.name}'", path.name)]
    files: list[Path] = _walk(path)[0]
    names: list[str] = [p.relative_to(path).as_posix() for p in files]
    unnamed: list[str] = [n for n in names if not _names(report_text, Path(n).name)]
    if not unnamed:
        return []
    listed: str = ", ".join(unnamed[:MAX_LISTED_UNREFERENCED])
    more: str = f", and {len(unnamed) - MAX_LISTED_UNREFERENCED} more" if len(unnamed) > MAX_LISTED_UNREFERENCED else ""
    return [_finding(str(path), 0, Category.ATTACHMENT_UNREFERENCED,
                     f"{len(unnamed)} of {len(names)} files are never named in the report: {listed}{more}", "")]


def _names(text: str, name: str) -> bool:
    """True when name appears in text as a whole token, so data.json does not count for a.json."""
    pattern: str = rf"(?<![A-Za-z0-9_.-]){re.escape(name)}(?![A-Za-z0-9_-]|\.[A-Za-z0-9])"
    return re.search(pattern, text) is not None


def hash_evidence(paths: list[Path]) -> list[HashEntry]:
    """Return SHA-256 and size for every evidence file, archives hashed as whole files."""
    entries: list[HashEntry] = []
    for path in paths:
        for file in _walk(path)[0]:
            try:
                digest: str
                size: int
                digest, size = _sha256(file)
            except OSError as error:
                entries.append(HashEntry(str(file), "", 0, _describe_error(error)))
                continue
            entries.append(HashEntry(str(file), digest, size, ""))
    return entries


def _sha256(file: Path) -> tuple[str, int]:
    """Hash in fixed-size chunks; hashlib.file_digest would need Python 3.11."""
    digest: hashlib._Hash = hashlib.sha256()
    size: int = 0
    with file.open("rb") as handle:
        for chunk in iter(lambda: handle.read(HASH_CHUNK_BYTES), b""):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def aggregate(findings: list[Finding], categories: frozenset[Category]) -> list[Finding]:
    """Collapse repeated findings of the given categories to one per source, listing the other lines."""
    later_lines: dict[tuple[str, Category], list[int]] = {}
    kept: list[Finding] = []
    for f in findings:
        key: tuple[str, Category] = (f.source, f.category)
        if f.category not in categories:
            kept.append(f)
        elif key not in later_lines:
            later_lines[key] = []
            kept.append(f)
        else:
            later_lines[key].append(f.line)
    result: list[Finding] = []
    for f in kept:
        lines: list[int] = later_lines.get((f.source, f.category), [])
        if not lines:
            result.append(f)
            continue
        shown: str = ", ".join(str(n) for n in lines[:MAX_LISTED_LINES])
        more: str = f" and {len(lines) - MAX_LISTED_LINES} more" if len(lines) > MAX_LISTED_LINES else ""
        note: str = f" (also on {len(lines)} more lines: {shown}{more})"
        result.append(Finding(f.source, f.line, f.category, f.message + note, f.excerpt))
    return result


def _finding(source: str, line: int, category: Category, message: str, excerpt: str) -> Finding:
    """Build a finding; masks tokens in every field before trimming, as the last guard against a leak."""
    trimmed: str = _shorten(" ".join(mask_secrets(excerpt).split()), MAX_EXCERPT)
    return Finding(mask_secrets(source), line, category, mask_secrets(message), trimmed)


def _shorten(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: limit - 3] + "..."


def render_text(findings: list[Finding], coverage: list[Coverage], hashes: list[HashEntry]) -> str:
    """Human-readable findings, a per-category count, the coverage summary, and the optional manifest."""
    out: list[str] = []
    for f in findings:
        location: str = f"{f.source}:{f.line}" if f.line else f.source
        out.append(f"{location}: [{f.category}] {f.message}")
        if f.excerpt and f.category is not Category.ATTACHMENT_UNREFERENCED:
            out.append(f"    | {f.excerpt}")
    counts: Counter[str] = Counter(str(f.category) for f in findings)
    summary: str = ", ".join(f"{name} {count}" for name, count in sorted(counts.items()))
    out.append("")
    out.append(f"{len(findings)} findings" + (f" ({summary})" if summary else "")
               + ". Each is a prompt for judgment, not a verdict.")
    out.append("")
    out.extend(_coverage_lines(coverage))
    if hashes:
        out.append("")
        out.append("SHA-256 manifest:")
        for h in hashes:
            if h.error:
                out.append(f"{'unreadable':<64}  {'-':>10}  {h.path} ({h.error})")
            else:
                out.append(f"{h.sha256}  {h.size:>10}  {h.path}")
    return "\n".join(out)


def _coverage_lines(coverage: list[Coverage]) -> list[str]:
    """One line per file and member; scanned files beyond MAX_LISTED_SCANNED are counted, never the others."""
    counts: Counter[ScanStatus] = Counter(c.status for c in coverage)
    totals: str = ", ".join(f"{status} {counts[status]}" for status in ScanStatus)
    out: list[str] = [f"Scan coverage ({totals}):"]
    listed_scanned: int = 0
    for c in coverage:
        if c.status is ScanStatus.SCANNED:
            listed_scanned += 1
            if listed_scanned > MAX_LISTED_SCANNED:
                continue
        detail: str = f" ({c.detail})" if c.detail else ""
        out.append(f"  {c.status:<8} {mask_secrets(c.path)}{detail}")
    if listed_scanned > MAX_LISTED_SCANNED:
        out.append(f"  ... and {listed_scanned - MAX_LISTED_SCANNED} more scanned")
    return out


def render_json(findings: list[Finding], coverage: list[Coverage], hashes: list[HashEntry]) -> str:
    """Machine-readable output with the same content as the text form."""
    payload: dict[str, object] = {
        "findings": [asdict(f) | {"category": str(f.category)} for f in findings],
        "counts": dict(Counter(str(f.category) for f in findings)),
        "coverage": [
            {"path": mask_secrets(c.path), "status": str(c.status), "detail": c.detail} for c in coverage
        ],
        "hashes": [asdict(h) for h in hashes],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    sys.exit(main())
