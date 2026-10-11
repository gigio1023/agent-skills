// Optional print-first style. Import report and supply your own content.
// Choose a font available in the rendering environment; no fonts are bundled.
#let report(
  title: none,
  subtitle: none,
  font: "Noto Sans CJK KR",
  lang: "ko",
  accent: rgb("#3157a5"),
  body,
) = {
  set document(title: title)
  set page(
    paper: "a4",
    margin: (x: 20mm, y: 18mm),
    footer: context align(right, text(size: 8pt, fill: rgb("#59616d"), counter(page).display("1"))),
  )
  set text(font: font, lang: lang, size: 10.5pt, fill: rgb("#20252c"))
  set par(leading: 0.72em)
  set heading(numbering: none)
  show heading.where(level: 1): it => block(above: 1.2em, below: 0.65em)[
    #text(size: 15pt, weight: "bold", fill: accent, it.body)
  ]
  show heading.where(level: 2): it => block(above: 1em, below: 0.5em)[
    #text(size: 12pt, weight: "bold", it.body)
  ]
  if title != none {
    block(below: 1em)[#text(size: 25pt, weight: "bold", title)]
  }
  if subtitle != none {
    block(below: 1.2em)[#text(size: 10pt, fill: rgb("#59616d"), subtitle)]
  }
  body
}
