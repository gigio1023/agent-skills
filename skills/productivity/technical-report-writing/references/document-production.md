# Document Production

Use when choosing an authoring/rendering route, producing a PDF, or delivering an editable document. PDF is an output format, not a requirement to first create HTML. Preserve an existing authoring source and use the simplest route that supports the actual content and recipient workflow.

## Choose the authoring route

| Reader/workflow need | Starting choice | Why / what to check |
| --- | --- | --- |
| A new print-first internal report with deliberate typography | Typst source → PDF | Native pagination, tables, figures, equations, citations; check font availability and inspect the compiled PDF |
| A paper, publication template, or complex existing mathematical manuscript | Existing LaTeX template with its documented engine | Preserve class, packages, references, and venue rules; use `credo-paper-plan` or release tooling only when their research-paper task actually applies |
| Repeated analysis whose code, figures, and text must stay together | Quarto with the appropriate PDF engine | Reuse the project's computation and cache policy; verify executed outputs and render to the requested formats |
| Colleagues will edit in Word or use tracked changes | DOCX, with a reference template when available | Use document styles, real tables and headings; export with Word or LibreOffice and check the exported PDF |
| A maintained Markdown source needs publication in several formats | Pandoc with an explicit PDF engine and reference styling | Conversion is not typesetting: inspect unsupported blocks, tables, cross-references, and citations |
| A structured generated form, invoice, or repeated fixed-layout record | ReportLab or existing PDF tooling | Explicit layout is useful here; use flow-based layout for long text and embed fonts |
| An interactive web analysis or an existing polished browser layout | HTML/React; browser PDF export only when a fixed copy is needed | Wait for data, fonts, and figures, adapt print styles, replace interaction-only content, inspect the PDF |
| A collaborative knowledge page | Its existing native editor or service | Keep the source of truth and authorized recipients; export only when a portable copy is needed |

These are local defaults, not a ranking of engines. Reuse a working project instead of migrating it merely to match the table. Choose Typst for an otherwise unconstrained new print-first report; choose DOCX first when recipient editing is the deciding need. Avoid creating all formats speculatively.

## Discover before compiling

Check available commands, existing templates, package manifests, and actual font families. Keep setup within the requested scope; do not install an entire global toolchain for a small document without a reason. A project-local or isolated dependency environment is useful when permitted. A missing renderer is a reason to select another suitable route or obtain setup approval, not to claim an unrendered source is the PDF.

Representative commands, after prerequisite discovery:

```bash
typst compile report.typ report.pdf
quarto render report.qmd --to pdf
pandoc report.md --pdf-engine=xelatex -o report.pdf
pandoc report.md --reference-doc=reference.docx -o report.docx
libreoffice --headless --convert-to pdf --outdir export report.docx
```

Use the engine and executable actually installed (`soffice` is another common LibreOffice executable). Pandoc's default PDF route uses LaTeX; selecting a different supported engine is explicit. Quarto also supports a Typst format, but its template/feature compatibility differs from its LaTeX PDF output. Check the project's format, not merely the `.pdf` suffix.

When no print template exists, [the optional Typst style](../assets/report.typ) provides A4 margins, readable type, heading hierarchy, and a page number. Import its `report` function, choose a font present in the build environment, and supply the document body. It has no compulsory sections, card layout, page limit, or invented data. Adapt typography to the actual reader instead of treating the example as a brand identity.

## Keep layout and evidence portable

Use a light, print-friendly page for print-first work unless requested otherwise. Dark screen styling does not mandate dark PDFs. Keep color meanings and contrast usable in the actual output, including monochrome printing when relevant. Use vector figures when supported and readable raster alternatives when not. Do not rasterize the whole document to bypass font or layout problems.

Keep Korean/CJK fonts and fallback choices explicit; check that glyphs are present and the final PDF embeds or reliably represents them. Keep text searchable/selectable where the format supports it. For generated content, escape text for the target engine; text taken from records is not raw Typst, TeX, or HTML code.

Flow long text and tables across pages deliberately. Repeat table headers where supported, keep captions with their figures, and avoid splitting the one comparison a reader needs to see together. Move or restructure content before shrinking it below a useful reading size. A concise report need not fit on one page.

Use one authoritative content/data workflow. Different outputs may use different layouts and renderers; they do not require separately maintained facts. Preserve source tables and figure generation code as appropriate. For interactive-to-static conversion, select the comparisons and visible conditions the document needs rather than printing disabled controls.

## Inspect the artifact, not just the build

Check expected sections, final text, calculations, tables, sources, and figures in the actual output. Inspect page count against any requested bound; no bound means no invented one-page constraint. Check the opening, page breaks, long tables, dense figures, and final page. For short documents, inspect every page. Search/text extraction catches missing content; rendered images reveal clipping, overlaps, small type, missing glyphs, and detached captions. Use both when each tests a real risk.

Exercise a representative long-text or multipage case when changing a template. A compiler returning success does not show that the layout remains readable. If accessibility, PDF/A, or another conformance level is requested, use the corresponding validator; ordinary rendering and text extraction are not conformance certification.

Use available `docx`, `pdf`, and `pdf-page-count` skills for their concrete operations, and `data-chart` or technical-figure skills for requested figures. Deliver the requested file and editable source, not merely instructions to run an exporter. Keep renderer/setup details in the delivery note unless the document itself is a production guide.

## Primary documentation

Checked 2026-09-15: [Typst documentation](https://typst.app/docs/), [Quarto PDF basics](https://quarto.org/docs/output-formats/pdf-basics.html), and [Pandoc: creating a PDF](https://pandoc.org/MANUAL.html#creating-a-pdf). They establish available routes and prerequisites. The routing defaults above favor maintained sources, recipient editing needs, and readable technical documents.
