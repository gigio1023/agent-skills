# Interface Checks

Use the existing project's commands and supported targets. Cover the changed behavior rather than manufacturing a universal test matrix.

- Build, type check, and lint the actual app/package. Verify that lint scans the intended UI files and loads its theme.
- Inspect the initial view and the states affected by the change: loading, empty, failure, sparse/dense data, selection, or completion. Exercise the state, not only its JSX branch.
- Check keyboard reachability, visible focus, meaningful control names, overlay focus return, and semantic headings/tables. A chart needs an accessible summary or data representation; color alone cannot carry status.
- Render at a relevant laptop and narrow viewport. Check overflow, truncated names, chart labels, long values, and touch targets. Use the project's supported browsers when browser behavior changed.
- For a dashboard, verify calculations independently of the rendering, preserve active filters in shared URLs where applicable, and ensure the heading/caption remains true after filtering.
- For an offline artifact, open the built file with networking disabled and inspect missing fonts, scripts, images, and navigation. A dev-server screenshot does not verify the distributable file.
- For a printed output, switch to the document-production path. Test the PDF itself; hidden tabs, hover values, and collapsed content cannot carry its main argument.

Use automated accessibility checks when available and inspect relevant interactions yourself. Automated tools do not establish complete accessibility or editorial clarity. Return concise observations of failures, not an inventory of hypothetical checks.
