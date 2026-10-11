# Coverage of Carlini's checklist

Carlini's [Research Paper Release Checklist](https://nicholas.carlini.com/writing/2022/paper-release-checklist.html) (2022-01-30) is a list the author runs before every release. Most of its items assume a person reading the paper. This table records which items `scripts/check_tex.py` checks (the Source checks step of credo-release), how, and which need artifact inspection, current requirements, or author knowledge beyond that scanner.

## Automated by the script

| Carlini's item (paraphrased) | Section of his list | Script check | Severity | Limits |
| --- | --- | --- | --- | --- |
| Check the paper title is correct | primary | Prints `\title{}` text | info | Correctness is the author's call; the script only surfaces the text |
| Disable author TODO note macros; no TODO or FIXME text | primary | `\todo`/`\fixme` macros; TODO, FIXME, XXX as whole words outside comments | error | Custom note macros with other names are not known to the script |
| Search the LaTeX build log for error, warning, undefined, missing | primary | `--log` scans each log line for those four words; error/undefined are errors, warning/missing are warnings | error / warning | Only when the author supplies the log; the script does not build the paper |
| Search for doubled words | primary | Adjacent identical words, case-insensitive, outside comments | warning | Legitimate repeats ("had had") are reported too; the author decides |
| Inspect lines with a question mark or double periods | primary | `..` that is not part of `...`; `??` | warning | Narrowed from his rule: single `?` is not reported, since it is ordinary prose |
| No merge conflicts (`<<<<`, `====`, `>>>>`) | primary | Line-initial 7-character markers | error | Markers indented or inside verbatim blocks are still reported |
| If blind, author names appear nowhere | conference | `--blind --author NAME` searches every line, comments excluded | error | Only the names given; affiliations, grant numbers, and self-citation phrasing stay manual |
| Uncomment the acknowledgments section | public release | An `acknowledg...` heading or environment inside a `%` comment | warning | Heuristic; a missing acknowledgments section is not detected |
| Abstract formatted correctly without LaTeX macros | arXiv | Lists `\macro` tokens found inside `\begin{abstract}...\end{abstract}` | warning | Also prints the abstract text so the author can paste it into the form |

Additions not in his list: the script follows `\input` and `\include` so multi-file papers are checked whole, and it strips comments so a TODO in a comment does not count.

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
grep -n -i -E 'error|warning|undefined|missing' main.log
```

Doubled-word detection has no single grep; read the abstract and introduction aloud instead.
