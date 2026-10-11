# Source Acquisition

Use the tools already available in the current environment. The library contract is independent of a particular downloader. These methods were checked on 2026-10-07; inspect current help or source documentation when a command differs.

## Discover and read with Hugging Face

The locally inspected HF CLI v2.1.1 exposes these commands:

```bash
hf papers --help
hf papers search "research topic" --limit 10 --format json
hf papers info 1706.03762 --format json
hf papers read 1706.03762
hf papers list --date today --limit 20 --format json
```

The number is an illustrative discovery batch, not a collection quota. `info` takes a base arXiv identifier and returns HF metadata. `list` (alias `ls`) returns the HF daily-papers feed for a date, week, or month; it is a curated feed of submitted papers, not a search. `--json` is shorthand for `--format json`. The inspected CLI has no paper download or version-pinning command; the tested version-suffixed identifier was not found. Generated fields such as `ai_summary` and `ai_keywords` are discovery aids, not paper-author claims. Verify bibliographic details, versions, and artifact URLs at the original source. `read` returns a Markdown rendering from HF; save it as a labeled derivative if useful, then obtain available originals separately. A successful `read` is not evidence that a PDF, LaTeX archive, or figures were saved.

HF is useful for AI papers; it does not replace a web search over proceedings, journals, author sites, and research posts. If `hf papers` is unavailable, continue through available web tools rather than blocking on installation. Sources: [HF CLI guide](https://huggingface.co/docs/huggingface_hub/en/guides/cli#hf-papers) and [v2.1.1 implementation](https://github.com/huggingface/huggingface_hub/blob/v2.1.1/src/huggingface_hub/cli/papers.py).

## Papers and supplements

Resolve the work's identity and version at its canonical landing page. For arXiv, use the version actually analyzed and follow that page's PDF and TeX Source links: for example, [1706.03762v7](https://arxiv.org/abs/1706.03762v7) links to `/pdf/1706.03762v7` and `/src/1706.03762v7`. Inspect the actual source response before naming or extracting it; do not assume that every submission offers a LaTeX archive. Keep a PDF-only or unavailable-source result labeled correctly. The [arXiv API manual](https://info.arxiv.org/help/api/user-manual.html#511-a-note-on-article-versions) explains version-specific identifiers.

For a conference or journal, inspect the official publication page for the paper, appendices, supplementary files, author manuscript, and code/data links. Save the available author or repository version when the publisher version cannot be obtained, and label which version it is. Preserve existing identifiers and license notices. Record unavailable files and the attempted location without inventing a mirror or claiming an abstract-only item was read in full.

Prefer complete original source archives: figures, bibliography files, and other dependencies may already be inside. Keep the archive even when extracting a reading copy. Inspect archive members before extraction; reject absolute paths, traversal paths, and escaping links, and extract only within the work's folder. Do not compile downloaded TeX or execute code just to archive it. Respect source rate limits and access requirements; individual retrieval is not bulk mirroring.

## Research posts and web pages

Save original HTML and the content assets needed to interpret the article, especially figures, equations, linked notebooks, and downloadable supplements. A raw HTTP response can be only a JavaScript shell; verify that the article text is present. A page with remote image links is not an offline copy of those images.

When already available, browser page-save or [SingleFile](https://github.com/gildas-lormeau/SingleFile) can retain a page and its embedded resources. Otherwise save the original HTML and the article's relevant assets using supported HTTP/browser tools. Keep a separately named reading copy if rewriting asset paths; record the original-to-local mapping in `source.md` when needed. A rendered DOM or print-to-PDF is a derivative and can supplement, but does not silently replace, the original response.

Check the saved article and representative figures without relying on the live website. Label a text-only capture, missing lazy-loaded images, unresolved external assets, or interactive content that cannot be preserved. Do not crawl navigation links, ad resources, or the entire site. Zotero's own distinction between metadata links and stored [web snapshots](https://www.zotero.org/support/attaching_files#web_snapshots) is useful here: recording a URL alone does not preserve a page.

## Associated code

Follow the publication or author's code link. Record the repository URL and an immutable commit, then preserve the associated code and license, usually as an archive of that commit. An archive is sufficient for reading when Git history is not needed; use an existing checkout or clone when the task benefits from it. Keep downloaded code separate from executable project code.

Inspect whether the snapshot includes submodules and Git LFS objects. Save relevant accessible missing objects when practical, otherwise list the exact gaps. Do not describe LFS pointer text as downloaded model weights, or a top-level archive as a recursive repository backup. Package installation, model downloads, and experiment execution are separate work. See [GitHub source-code archives](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives) and [Git LFS in archives](https://docs.github.com/en/enterprise-cloud%40latest/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/managing-git-lfs-objects-in-archives-of-your-repository).

## Verify and leave a small record

Download into a temporary filename, check the response and actual file type, then move it to its versioned destination without overwriting earlier originals. Open or parse enough content to establish that it is the intended artifact. Hash the saved bytes rather than treating HTTP ETags as a portable checksum contract. Reuse byte-identical files already in the library.

For each work, put the canonical identity, capture/version information, reading coverage, and a brief finding in `source.md`. A small table is enough for artifacts:

```markdown
| Artifact | Local file | Origin / revision | Verification or gap |
| --- | --- | --- | --- |
| PDF | [paper-v1.pdf](paper-v1.pdf) | Versioned original URL | PDF opened; SHA-256: ... |
| Source and figures | [source-v1.tar.gz](source-v1.tar.gz) | Versioned source URL | Archive inspected; SHA-256: ... |
| Code | — | Author's repository URL | Unavailable: stated access error |
```

Include only relevant rows and replace illustrative values with observed facts. A single archive hash can cover a bundle; do not build an inventory database for individual images. Extract text when useful and available, keeping page/section locators and any extraction failures. Validate the local index and artifact links before reporting collection complete.
