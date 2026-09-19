# quarto-lecture-notes

Shared design and build configuration for my Quarto lecture-note books:
[or-book](https://github.com/zi-ang-liu/or-book),
[rl-book](https://github.com/zi-ang-liu/rl-book),
[data-science-book](https://github.com/zi-ang-liu/data-science-book),
[computer-literacy-book](https://github.com/zi-ang-liu/computer-literacy-book) and
[database-book](https://github.com/zi-ang-liu/database-book) — and for two
repos that are not course books but use the same design and conventions:
`math-note`, a private notebook that publishes nothing, and
[jb-open-campus](https://github.com/zi-ang-liu/jb-open-campus), the mock
lectures for high-school students at the department's open campus.

Each book keeps its own repo. Everything the books had in common — theme, colours,
fonts, PDF settings, author block, footer, CI — lives here instead, so a design
change is one commit in one place.

**[CONVENTION.md](CONVENTION.md)** is the writing standard for the books —
when to use a callout, a theorem environment, or a plain heading, and the
cross-reference prefixes for each. `python3 scripts/lint-conventions.py ~/Github`
checks the mechanical rules.

## What's in here

| File | Owns |
|---|---|
| `_extensions/lecture/_extension.yml` | The `lecture-html` and `lecture-pdf` formats |
| `_extensions/lecture/_brand.yml` | Colours, fonts, root font size (light + dark) |
| `_extensions/lecture/theme.scss` | Layout, spacing, callouts, theorem blocks — light |
| `_extensions/lecture/theme-dark.scss` | The same, for the dark toggle |
| `_extensions/lecture/preamble.tex` | `algorithm` / `algpseudocode` setup for PDF |
| `_extensions/lecture/_book.yml` | Shared `book:` keys (author, footer, search, sidebar) |
| `.github/workflows/book.yml` | Reusable build-and-publish workflow |
| `.github/workflows/rebuild-all.yml` | Redeploys every published repo when the design changes |

The split between `_brand.yml` and `theme.scss` is deliberate: **colours and fonts
only in the brand file, structure only in the SCSS.** The SCSS mirrors the palette
names (`$indigo`, `$mist`, …) with `!default` so it still compiles if the brand file
is ever missing, but the brand file always wins. To recolour every book at once,
edit `_brand.yml` and nothing else.

## Using it in a book repo

```bash
quarto add zi-ang-liu/quarto-lecture-notes
```

That installs into `_extensions/zi-ang-liu/lecture/`. Then the book's `_quarto.yml`
keeps only what is genuinely specific to that book:

```yaml
project:
  type: book

lang: ja
brand: _extensions/zi-ang-liu/lecture/_brand.yml
bibliography: references.bib

execute:
  freeze: auto

metadata-files:
  - _extensions/zi-ang-liu/lecture/_book.yml

format:
  lecture-html: default
  lecture-pdf: default

book:
  title: "Database Systems"
  cover-image: cover.png
  site-url: https://zi-ang-liu.github.io/database-book/
  repo-url: https://github.com/zi-ang-liu/database-book
  chapters:
    - index.qmd
    # ...
```

Three lines carry the shared setup, and each has a reason:

- **`brand:`** — a format extension cannot register a brand on its own. The
  `theme:` list inside the extension asks for a `brand` layer, and this line is what
  tells Quarto where to find it. Without it the books silently fall back to the
  plain `cosmo` blue and Source Sans Pro.
- **`metadata-files:`** — a format extension can only contribute keys under
  `format:`, never project-level `book:` keys, so the shared author block and footer
  come in this way.
- **`format: lecture-html`** — the formats themselves.

Anything set in the book's own `_quarto.yml` overrides this repo. rl-book, for
example, sets an English author name and `lang: en` locally.

Books that use the pseudocode filter still install it separately — Quarto extensions
can't depend on other extensions:

```bash
quarto add leovan/quarto-pseudocode
```

## CI

Add this as `.github/workflows/publish.yml` in each book repo:

```yaml
name: Publish
on:
  push:
    branches: [main]
  repository_dispatch:
    types: [theme-updated]
  workflow_dispatch:

jobs:
  book:
    # Required. A reusable workflow cannot request more permission than the
    # calling job holds, so publishing to gh-pages has to be granted here —
    # otherwise the run fails to even start with "is requesting
    # 'contents: write', but is only allowed 'contents: read'".
    permissions:
      contents: write
    uses: zi-ang-liu/quarto-lecture-notes/.github/workflows/book.yml@main
    with:
      update-extensions: ${{ github.event_name == 'repository_dispatch' }}
```

Books with executed Python chunks also need `python-version: "3.12"` and a
`requirements.txt`: `_freeze/` is committed, but CI re-executes any chapter
whose source changed since its freeze.

`rebuild-all.yml` here fires a `theme-updated` dispatch at every published repo
(the five books and jb-open-campus) whenever `_extensions/**` changes on `main`.
It needs a repository secret `BOOKS_DISPATCH_TOKEN` — a fine-grained PAT scoped
to those repos with *Contents: read and write*. A repo added to the workflow's
matrix has to be added to the PAT as well.

Normal pushes render with the extension version committed in the book repo, so local
and CI output agree. Only a `theme-updated` rebuild pulls the newest extension. To
bring the committed copies up to date:

```bash
./scripts/update-books.sh --commit
```

## Releasing a change

1. Edit `_brand.yml` / `theme.scss` here.
2. Bump `version:` in `_extension.yml`, commit, push.
3. `rebuild-all.yml` redeploys every published repo.
4. Run `./scripts/update-books.sh --commit` when convenient, and push each repo.
