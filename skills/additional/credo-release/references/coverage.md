# Coverage of Carlini's checklist

Carlini's [Research Paper Release Checklist](https://nicholas.carlini.com/writing/2022/paper-release-checklist.html) (2022-01-30) is a list the author runs before every release. Most of its items assume a person reading the paper. This table records which items `scripts/check_tex.py` checks (the Source checks step of credo-release), how, and which need artifact inspection, current requirements, or author knowledge beyond that scanner.

## Automated by the script

| Carlini's item (paraphrased) | Section of his list | Script check | Severity | Limits |
| --- | --- | --- | --- | --- |
| Check the paper title is correct | primary | Prints `\title{}` text | info | Correctness is the author's call; the script only surfaces the text |
| Disable author TODO note macros; no TODO or FIXME text | primary | `\todo`/`\fixme` macros outside their own definitions; TODO, FIXME, XXX as whole words outside comments | error | Custom note macros with other names are not known to the script |
| Search the LaTeX build log for error, warning, undefined, missing | primary | `--log` reports LaTeX error, warning, and missing-character lines by their log form | error / warning | Only when the author supplies the log; the script does not build the paper |
| Search for doubled words | primary | Adjacent identical words, case-insensitive, outside comments | warning | Legitimate repeats ("had had") are reported too; the author decides |
| Inspect lines with a question mark or double periods | primary | `..` that is not part of `...`; `??` | warning | Narrowed from his rule: single `?` is not reported, since it is ordinary prose |
| No merge conflicts (`<<<<`, `====`, `>>>>`) | primary | Line-initial 7-character markers | error | Markers indented or inside verbatim blocks are still reported |
| If blind, author names appear nowhere | conference | `--blind --author NAME` searches every line, comments excluded | error | Only the names given; affiliations, grant numbers, and self-citation phrasing stay manual |
| Uncomment the acknowledgments section | public release | An `acknowledg...` heading or environment inside a `%` comment | warning | Heuristic; a missing acknowledgments section is not detected |
| Abstract formatted correctly without LaTeX macros | arXiv | Lists `\macro` tokens found inside `\begin{abstract}...\end{abstract}` | warning | Also prints the abstract text so the author can paste it into the form |

Additions not in his list: the script follows `\input` and `\include` so multi-file papers are checked whole, and it strips comments so a TODO in a comment does not count.

Two checks match forms rather than bare words, so ordinary text that mentions a keyword is not a finding:

- TODO macros: the macro name inside its own `\newcommand`, `\renewcommand`, `\providecommand`, or `\def` definition is skipped. The disabled form `\renewcommand{\todo}[1]{}` from his list passes, while a later `\todo{...}` call is still an error.
- Build log: errors are lines starting with `! ` and, under `-file-line-error`, `file:line:` lines. Warnings are `LaTeX`, `Package`, or `Class` lines containing `Warning:`, `pdfTeX warning` lines, and `Missing character:` notices. A warning about an undefined reference or citation counts as an error, and the closing "There were undefined references" or "There were undefined citations" summary line still catches one whose own warning wrapped onto a continuation line. `Package:`, `File:`, and `Document Class:` banner lines are skipped, so a package description such as infwarerr's "info/warning/error messages" is not a finding.

## Outside the bundled scanner

These need a rendered PDF, the build itself, current venue requirements, or knowledge the script does not have. An agent may inspect available artifacts with suitable tools; only actual author answers count as author confirmation:

- Visual layout: paragraphs ending with a single word on a new line; a single line stranded at the top of a page under a caption.
- Captions understandable in near-isolation after late edits.
- PDF rendered on another computer; fonts embedded; figures legible; Type 3 fonts absent when the venue cares.
- Page count against the limit, including separate rules for appendix and references; page numbering per the call for papers; bibliography style; blind or non-blind rules; any anonymous author field required by the actual venue.
- Author list complete; names and affiliations spelled correctly; author block does not break page one; copyright block added (camera-ready) or removed (arXiv); accepted-version template in use.
- arXiv form: whether to strip comments before upload; names on the form match the paper; rendered arXiv PDF matches the local build.

## Manual equivalents when Python is unavailable

```bash
grep -n -E '<<<<<<<|=======|>>>>>>>' *.tex
grep -n -E '\b(TODO|FIXME|XXX)\b|\\todo' *.tex
grep -n -E '\?\?|(^|[^.])\.\.([^.]|$)' *.tex
grep -n -E '^! |^[^ ]+\.[a-z]+:[0-9]+: |Warning:|pdfTeX warning|^Missing character:' main.log
```

Doubled-word detection has no single grep; read the abstract and introduction aloud instead.
