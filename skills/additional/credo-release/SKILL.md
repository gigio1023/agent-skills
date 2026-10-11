---
name: credo-release
description: "Check a LaTeX paper before submission, camera-ready, or arXiv release: run bundled source checks, inspect the rendered artifact and current venue requirements, and ask for author-only attestations. Use for final checks or linting TeX. NOT for argument planning (credo-paper-plan), a LaTeX report or result bound for a customer or other external reader (evaluation-audit release mode), automatic paper rewriting, or submission without authorization."
---

# Credo: Release

Return a release review with evidence for checked items and the remaining author decisions. Adapted from Carlini's [Research Paper Release Checklist](https://nicholas.carlini.com/writing/2022/paper-release-checklist.html); see [coverage](references/coverage.md) for the bundled script's limits.

Scope: a paper or preprint headed to a venue or arXiv. A customer, technical, or evaluation report typeset in LaTeX goes to evaluation-audit release mode, which decides whether its results can be shown; the source scanner below can still lint that report's TeX when asked.

## Source checks

From this skill directory:

```bash
python3 scripts/check_tex.py path/to/main.tex --log path/to/main.log
python3 scripts/check_tex.py path/to/main.tex --blind --author "Full Name"
```

Python 3.10 or newer; no packages. The script follows `\input` and `\include`, strips comments, and prints severity, location, and message plus a summary. Exit 1 means an error finding; 2 means invalid usage. It catches source markers, potential text mistakes, selected anonymity clues, and supplied build-log issues. Warnings need interpretation; it cannot establish venue compliance or scientific correctness.

Report the command and actionable findings. Rerun affected checks after authorized edits. If Python is unavailable, inspect by the alternatives in the coverage reference and state the narrower coverage.

## Artifact and author checks

Use [the release checklist](references/manual-checklist.md) for the actual release type. Inspect available artifacts directly with suitable tools: PDF rendering, page count, fonts, captions, links, title/form comparison, and applicable venue rules. Check the current official requirements when needed; a remembered page limit or anonymous-author format is insufficient.

Record `checked` only with the actual observation, `confirmed by author` only for an author answer, `open` for an unresolved item, and `n/a` with the applicable reason. Do not infer rendered layout from source or claim another-machine verification from one local render. Ask only for items requiring unavailable material or human attestation, such as agreement to authorship or the final submission declaration; bundle related missing answers rather than walking the user through checks already completed.

Keep new recurring mistakes in a project checklist when that maintenance is authorized. Do not silently edit an installed shared package from a paper's release review.

## Output and authority

Lead with release-blocking findings, then the compact checked/open record needed by the author. Distinguish an actual defect from unavailable evidence. A review does not authorize rewriting, uploading, submitting, or certifying on the author's behalf. If fixes or submission were already requested, preserve that authority and complete only the requested actions; structural argument work can use `credo-paper-plan`.
