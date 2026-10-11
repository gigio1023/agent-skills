# Artifact and author checklist

Adapted from Carlini's [Research Paper Release Checklist](https://nicholas.carlini.com/writing/2022/paper-release-checklist.html) (2022-01-30). These items are outside the bundled text scanner. Inspect those supported by available tools; reserve author confirmation for human-only decisions or evidence the agent cannot access. Items a program can check (TODO markers, merge-conflict markers, doubled words, `..` and `??`, blind author names, abstract macros, commented-out acknowledgments, build-log words) are run by the script in the Source checks step; see coverage.md. Keep project-specific additions in an authorized project checklist.

## Every release

- Title is correct: compare the printed `\title{}` text against the submission form or accepted title.
- Build log is clean, if it was not given to the script: search it for error, warning, undefined, missing.
- No paragraph ends with a single word on its own line; no single line is stranded at the top of a page under a caption (open the PDF).
- Every caption is understandable in near-isolation and late edits did not break one (read only the captions).
- The PDF renders on another computer: fonts embedded, figures legible.

## Conference submission

- Call for papers checked for blind versus non-blind rules; if blind, also check affiliations, grant numbers, repository links, and self-citation phrasing, which the script does not know.
- Page numbering follows the call for papers.
- Page count is within the limit, with separate rules for appendix and references versus content pages.
- Bibliography style matches the venue.
- Use the actual venue-required anonymous author field and submission identifier, if any; do not infer a format from the research field.

## Public release (camera-ready)

- All authors listed; names spelled correctly; affiliations correct.
- Template switched to the accepted version of the style.
- Author block does not break the flow of page one.
- Copyright block or publication notice added as the venue requires.
- Type 3 fonts absent if the venue cares (`pdffonts` or the venue's checker).
- Acknowledgments and author-contribution sections are present and uncommented (the script flags a commented heading; confirm by reading the PDF).

## arXiv upload

- Decide whether to strip LaTeX comments before upload.
- Author names on the upload form match the paper, allowing the authors' preferred ASCII variants.
- Copyright block removed if the venue's terms require it for preprints.
- Abstract on the form has no LaTeX macros (paste the text the script printed).
- The rendered arXiv PDF matches the local build.

## Added later

When checklist maintenance is requested, record the date, mistake, and useful check in the project record.
