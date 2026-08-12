# CLAUDE.md — quarto-lecture-notes

This repo is the **hub** for five Quarto lecture-note books. It holds the shared
design, the shared build, and the writing conventions. Nothing here is a book.

## The system

```
quarto-lecture-notes                    ← you are here
├── _extensions/lecture/
│   ├── _extension.yml   lecture-html + lecture-pdf formats
│   ├── _brand.yml       colours, fonts, root size  ← edit here to restyle all 5
│   ├── theme.scss       layout, callouts, theorem blocks (light)
│   ├── theme-dark.scss  the same, dark
│   ├── _book.yml        shared book: keys (author, footer, search, sidebar)
│   └── preamble.tex     algorithm/algpseudocode for PDF
├── CONVENTION.md        ← the writing standard. Read before editing any .qmd
├── scripts/
│   ├── lint-conventions.py   mechanical checks across all five books
│   └── update-books.sh       quarto update across local clones
├── templates/gitignore  the identical .gitignore all five books use
└── .github/workflows/
    ├── book.yml         reusable build+publish, called by each book
    └── rebuild-all.yml  dispatches theme-updated to all five on _extensions/** change
```

The five books live beside this repo:

    ~/Github/{or-book,rl-book,data-science-book,computer-literacy-book,database-book}

They are **separate git repos**, each consuming this one as a Quarto extension at
`_extensions/zi-ang-liu/lecture/`.

## Start here

```bash
python3 scripts/lint-conventions.py ~/Github
```

0 errors / 0 warnings is the current baseline. Any finding is a regression.

## Changing the design

1. Edit `_brand.yml` (colours, fonts) or `theme.scss` (layout, spacing).
   **Colours and fonts only in the brand file; structure only in the SCSS.**
2. Bump `version:` in `_extensions/lecture/_extension.yml`.
3. Commit and push. `rebuild-all.yml` fires `theme-updated` at all five books,
   each pulls the new extension and redeploys — usually under two minutes.
4. `./scripts/update-books.sh --commit` brings each book's committed
   `_extensions/` up to date, then push each book.

Pushing a change under `_extensions/**` **deploys to five live course sites.**
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
- `rebuild-all.yml` needs the `BOOKS_DISPATCH_TOKEN` secret (fine-grained PAT,
  the five book repos, Contents: read and write).

## Decisions already made — do not "fix" these

- **Callout and `#rem-`/`#alg-` cross-references render in English** in the
  Japanese books. A working `crossref: custom:` recipe is in CONVENTION.md §4,
  deliberately **not applied**: callouts are skippable, so they are rarely cited.
- **Callouts carry no icon and use body-sized text.** `callout-icon: false` in
  `_extension.yml` covers HTML and PDF; the `.9rem` override is in both SCSS
  files. Don't reintroduce either.
- **computer-literacy-book has no theorem-type environments on purpose.**
  Numbered 定義 X.Y reads as too formal for a first-year course.

## Environment

- Renders that execute code need `QUARTO_PYTHON=/opt/miniconda3/envs/quarto-book/bin/python`.
  The system `python3` has no jupyter. That env is Python **3.10**, which is
  what each book's `publish.yml` requests and what `requirements.txt` pins
  against — keep the three in step.
- `gh` is installed and authenticated as `zi-ang-liu`, so a push is verifiable
  from here. Don't guess whether a build passed:

  ```bash
  gh run list --limit 3                 # from the book's directory
  gh run watch <run-id> --exit-status   # blocks until the run finishes
  gh run view <run-id> --log            # e.g. to confirm _freeze/ spared
                                        # CI from executing any Python
  ```
