# Interaction and Static Delivery

Use when the reader can change selections or when a dashboard also needs a fixed document.

## Keep selections and claims aligned

Persist meaningful filters in the URL for a shareable hosted app. Show active selections and a meaningful population count. Linked panels should update consistently, or visibly indicate that they show a separate population. A reset control should restore an informative default, not an arbitrary empty canvas.

Derived headlines, rankings, percentages, captions, and summaries must describe the displayed selection. Recompute them from the same filtered data, or separate a fixed editorial comparison from the exploratory section. Test a normal selection, a materially different one, and an empty selection. Do not retain a stale headline and compensate with a footnote about how the UI works.

Use standard controls and local labels. Essential interpretation cannot exist only in a tooltip or color. Offer a clear empty/error state and preserve the distinction between zero results, missing data, and unavailable data.

## Turn exploration into a printable argument

Choose the comparisons the document should communicate. State the selected period/population where it matters. Replace tabs and hover details with visible panels, annotations, or a concise table. Remove disabled filters and application chrome rather than printing a screenshot of the app. Keep an important contrary result in the reading path.

Reuse source data and transformations across outputs, not necessarily one visual layout or one component tree. A print document can use a different chart arrangement and a light theme. The same series should retain a recognizable label and meaning, with colors adjusted for contrast on the new background.

Use vector charts when the renderer supports them. Inspect the actual PDF for clipped marks, unreadable labels, broken page boundaries, lost citations, and missing selected data. The PDF must explain the result without the web page.

Sources: [Segel and Heer, section 4.4](https://idl.uw.edu/papers/narrative) describes author-driven narrative followed by reader-driven exploration; [Vercel Web Interface Guidelines](https://vercel.com/design/guidelines) supports URL state, accessible labels, and working interaction states. Neither implies that every report needs interaction.
