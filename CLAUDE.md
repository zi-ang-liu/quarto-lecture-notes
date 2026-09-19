# CLAUDE.md — quarto-lecture-notes

This repo is the **hub** for five Quarto lecture-note books, one private
notebook and the open-campus mock lectures. It holds the shared design, the
shared build, and the writing conventions. Nothing here is a book.

## The system

```
quarto-lecture-notes                    ← you are here
├── _extensions/lecture/
│   ├── _extension.yml   lecture-html + lecture-pdf + lecture-revealjs formats
│   ├── _brand.yml       colours, fonts, root size  ← edit here to restyle all 5
│   ├── theme.scss       layout, callouts, theorem blocks (light)
│   ├── theme-dark.scss  the same, dark
│   ├── theme-revealjs.scss   slides: projector sizing, title rule, footer
│   ├── lecture-revealjs.lua  slides: paints the title and section slides
│   ├── footer.html      slides: running footer filled from the subtitle
│   ├── _book.yml        shared book: keys (author, footer, search, sidebar)
│   └── preamble.tex     algorithm/algpseudocode for PDF
├── CONVENTION.md        ← the writing standard. Read before editing any .qmd
├── scripts/
│   ├── lint-conventions.py   mechanical checks across all seven repos
│   └── update-books.sh       quarto update across local clones
├── templates/gitignore  the identical .gitignore all seven repos use
└── .github/workflows/
    ├── book.yml         reusable build+publish, called by each book
    └── rebuild-all.yml  dispatches theme-updated to the six published repos
                         on _extensions/** change
```

The five books live beside this repo:

    ~/Github/{or-book,rl-book,data-science-book,computer-literacy-book,database-book}

They are **separate git repos**, each consuming this one as a Quarto extension at
`_extensions/zi-ang-liu/lecture/`.

`~/Github/math-note` consumes the extension the same way and follows the same
conventions, but it is **not** a course book: a private, English, local-only
notebook with no `site-url`, no `publish.yml`, and no deployed site. It is in
`lint-conventions.py` and `update-books.sh`, and deliberately **not** in
`rebuild-all.yml` — dispatching `theme-updated` at a repo with no publish
workflow does nothing. See its own `CLAUDE.md`.

`~/Github/jb-open-campus` is the third kind: the 模擬授業 (mock lectures) for
high-school students at the department's open campus, one chapter per lecture.
Same extension, same conventions, published like a book — so it **is** in
`rebuild-all.yml` — but by design it has **no theorem-type environments**
(titled callouts instead; numbered 例 X.Y is too formal for that audience) and
hides all code (`echo: false`). The `jb-` prefix is a leftover from the
Jupyter Book version it replaced in September 2026. See its own `CLAUDE.md`.

## Start here

```bash
python3 scripts/lint-conventions.py ~/Github
```

0 errors / 0 warnings is the current baseline. Any finding is a regression.

## Changing the design

1. Edit `_brand.yml` (colours, fonts) or `theme.scss` (layout, spacing).
   **Colours and fonts only in the brand file; structure only in the SCSS.**
2. Bump `version:` in `_extensions/lecture/_extension.yml`.
3. Commit and push. `rebuild-all.yml` fires `theme-updated` at the five books
   and jb-open-campus; each pulls the new extension and redeploys — usually
   under two minutes.
4. `./scripts/update-books.sh --commit` brings each book's committed
   `_extensions/` up to date, then push each book.

Pushing a change under `_extensions/**` **deploys to six live sites.**
Confirm with the author before pushing unless they have already asked for it.

## Gotchas that cost time before

- A local render can reuse a **cached compiled stylesheet** and show the old
  colours. `rm -rf .quarto` in the book, then render.
- A format extension **cannot** register a brand by itself. Each book needs
  `brand: _extensions/zi-ang-liu/lecture/_brand.yml` at project level, or fonts
  silently fall back to Source Sans Pro.
- A format extension can only contribute keys under `format:` — never project
  level `book:` keys. Those come from `_book.yml` via `metadata-files:`.
- The reusable workflow needs `permissions: contents: write` **on the calling
  job** in each book. A reusable workflow cannot request more than its caller
  holds, and the run is rejected before any step executes.
- Slides (`lecture-revealjs`) load KaTeX from jsdelivr. **No wifi, no math.**
  `embed-resources: true` does not help — it yields a 32 MB file that still
  fetches KaTeX. The fix is to ship KaTeX inside this extension (~600 KB with
  woff2 fonts only) and point `html-math-method.url` at it; not done yet.
- `rebuild-all.yml` needs the `BOOKS_DISPATCH_TOKEN` secret (fine-grained PAT,
  every repo in its matrix, Contents: read and write). A repo added to the
  matrix but not to the PAT fails its dispatch with 404.
- A figure drawn by a code cell is a plain `<img>` with its pixel size written
  in — no `img-fluid`, unlike a Markdown image — so a plot wider than the
  46rem column used to push a horizontal scrollbar under itself (rl-book's
  10-inch plots, every phone). `theme.scss` and `theme-dark.scss` now cap
  `.cell-output-display img` at `max-width: 100%` (extension 1.3.1).
- Wikimedia rate-limits pandoc's image fetches (HTTP 429), so a **PDF** render
  of a chapter that hot-links Wikimedia images fails. HTML is unaffected — the
  browser fetches them — but ship local copies of CC-licensed images if the
  PDF matters. jb-open-campus is the live case.
- conda's `defaults` channel now refuses to solve until Anaconda's ToS is
  accepted. Build envs with `--override-channels -c conda-forge` instead.
- scipy 1.15.x PyPI wheels do not load on macOS 27 (dyld rejects their
  `__thread_bss` section; seen with the 3.10 and 3.12 wheels). The books pin
  1.16.3 for that reason; conda-forge never built 1.15.3 for osx-arm64 either.
  scipy >= 1.16 needs Python >= 3.11, so the books cannot go back to 3.10.

## Decisions already made — do not "fix" these

- **Callout and `#rem-`/`#alg-` cross-references render in English** in the
  Japanese books. A working `crossref: custom:` recipe is in CONVENTION.md §4,
  deliberately **not applied**: callouts are skippable, so they are rarely cited.
- **Callouts carry no icon and use body-sized text.** `callout-icon: false` in
  `_extension.yml` covers HTML and PDF; the `.9rem` override is in both SCSS
  files. Don't reintroduce either.
- **computer-literacy-book has no theorem-type environments on purpose.**
  Numbered 定義 X.Y reads as too formal for a first-year course. The same
  holds for jb-open-campus, whose readers are high-school students.

## Environment

- Renders that execute code need `QUARTO_PYTHON=/opt/miniconda3/envs/quarto-book/bin/python`.
  The system `python3` has no jupyter. That env is Python **3.12**, which is
  what each book's `publish.yml` requests and what `requirements.txt` pins
  against — keep the three in step. To rebuild it:

  ```bash
  conda create -n quarto-book --override-channels -c conda-forge python=3.12 pip
  /opt/miniconda3/envs/quarto-book/bin/pip install \
      -r ~/Github/or-book/requirements.txt \
      -r ~/Github/rl-book/requirements.txt \
      -r ~/Github/data-science-book/requirements.txt
  ```
- `gh` is installed and authenticated as `zi-ang-liu`, so a push is verifiable
  from here. Don't guess whether a build passed:

  ```bash
  gh run list --limit 3                 # from the book's directory
  gh run watch <run-id> --exit-status   # blocks until the run finishes
  gh run view <run-id> --log            # e.g. to confirm _freeze/ spared
                                        # CI from executing any Python
  ```
