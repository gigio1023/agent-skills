#!/usr/bin/env python3
import argparse
import re
import subprocess
import sys


def count_with_pypdf(path: str) -> int | None:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        try:
            from PyPDF2 import PdfReader  # type: ignore
        except Exception:
            return None
    reader = PdfReader(path)
    return len(reader.pages)


def count_with_pdfinfo(path: str) -> int | None:
    try:
        out = subprocess.check_output(["pdfinfo", path], text=True, stderr=subprocess.STDOUT)
    except Exception:
        return None
    match = re.search(r"^Pages:\s+(\d+)\s*$", out, re.MULTILINE)
    if not match:
        return None
    return int(match.group(1))


def count_with_mdls(path: str) -> int | None:
    try:
        out = subprocess.check_output(
            ["mdls", "-name", "kMDItemNumberOfPages", path],
            text=True,
            stderr=subprocess.STDOUT,
        )
    except Exception:
        return None
    match = re.search(r"kMDItemNumberOfPages = (\d+)", out)
    if not match:
        return None
    return int(match.group(1))


def main() -> int:
    parser = argparse.ArgumentParser(description="Count pages in a PDF.")
    parser.add_argument("pdf_path", help="Path to PDF file")
    args = parser.parse_args()

    for counter in (count_with_pypdf, count_with_pdfinfo, count_with_mdls):
        pages = counter(args.pdf_path)
        if pages is not None:
            print(pages)
            return 0

    print("Error: could not determine PDF page count. Install pypdf or ensure pdfinfo is available.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
