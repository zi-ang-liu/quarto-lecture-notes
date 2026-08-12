# Writing conventions

House rules for the five lecture-note books
([or-book](https://github.com/zi-ang-liu/or-book),
[rl-book](https://github.com/zi-ang-liu/rl-book),
[data-science-book](https://github.com/zi-ang-liu/data-science-book),
[computer-literacy-book](https://github.com/zi-ang-liu/computer-literacy-book),
[database-book](https://github.com/zi-ang-liu/database-book)).

Everything here was checked against Quarto 1.9.38 with the `lecture` extension
and `lang: ja`.

---

## 1. Which form for which content

The single decision that matters. All three forms produce a box; they mean
different things to a student.

| The content is… | Use | Why |
|---|---|---|
| Something the student **must know**, that you may want to point back to | a **theorem-type** block (`#def-`, `#thm-`, `#exm-`, `#exr-`…) | numbered, cross-referenceable, indexed as course material |
| **Chapter structure** — 学習目標, まとめ | a plain `##` **heading section** | appears in the sidebar TOC, so students can jump to it |
| **Skippable enrichment** — history, external links, tool tips, a pitfall | a **callout**, always titled | signals "you may skip this" |

A callout never appears in the sidebar TOC: a leading heading inside it is
absorbed into the callout title. That is the main reason 学習目標 is a section
and not a callout.

**Do not put core content in a callout.** A definition or a proposition inside
`callout-note` reads as optional and cannot be referenced.

---

## 2. Theorem-type environments

Numbered, boxed, cross-referenceable. The label prefix chooses the environment —
there is no class to write.

| Prefix | Printed (`lang: ja`) | Printed (`lang: en`) | LaTeX environment |
|---|---|---|---|
| `#thm-` | 定理 | Theorem | `theorem` |
| `#lem-` | 補題 | Lemma | `lemma` |
| `#cor-` | 系 | Corollary | `corollary` |
| `#prp-` | 命題 | Proposition | `proposition` |
| `#cnj-` | 予想 | Conjecture | `conjecture` |
| `#def-` | 定義 | Definition | `definition` |
| `#exm-` | 例 | Example | `example` |
| `#exr-` | 練習 | Exercise | `exercise` |
| `#alg-` | *(not localized — prints "Algorithm"; accepted, see §4)* | Algorithm | `algorithm` |

```markdown
::: {#def-relation}
リレーション $R$ とは，$D_1 \times \cdots \times D_n$ の部分集合である．
:::

@def-relation より，…
```

An optional `## Title` as the first line becomes the environment's name:
`例 15.1 (最適化問題の例)`.

### Examples, exercises and problem sets

Three forms carry problems. They differ on **who does the work**, and one test
separates them:

| Form | The test | Numbered | Answer |
|---|---|---|---|
| `#exm-` | **The author answers it.** The reader only reads. | 例 15.1 | inside the block |
| `#exr-` | The reader does it. | 練習 15.1 | a separate `#sol-` |
| numbered list under `## 練習問題` | four or more short, homogeneous drills done as one batch | no | one answer set for the batch |

**An `#exm-` must never end on an unanswered question.** That is the line
between the first two rows. A block that poses a problem and stops is an
exercise, whatever its label says — and because Quarto numbers 例 and 練習 in
separate sequences, mislabelling it also makes the chapter's exercise count
wrong for the student.

Posing a question inside an `#exm-` is fine, and usually good writing — as long
as the same block answers it:

```markdown
:::{#exm-newsvendor-cost}
発注量 $S = 100$ … のとき，コスト $g(S, d)$ は以下のように求められる．
$$ g(100, 120) = 100 $$
:::
```

Do **not** convert drill sets into individual `#exr-` blocks. Six one-line SQL
problems of the same skill, graded as one assignment, belong in a numbered
list — six numbered frames would be noise. Reach for `#exr-` when a problem is
substantial enough to reference or answer on its own.

### Solutions

**Give most `#exr-` a `#sol-`.** Two exceptions:

- **Thought problems** — 思考実験 and open-ended discussion prompts, where the
  point is the reasoning in class, not a final answer.
- **Very simple problems** — one-step drills whose answer the student can
  check immediately.

Keep the `#sol-` adjacent to the `#exr-` it answers. Note that `#sol-` is a
proof-type environment, so it renders as an inline italic *解答.* rather than a
box — it will not look like the exercise it follows.

### Proof-type environments

`proof`, `remark` and `solution` are **not** theorem-type. They render as an
inline italic run-in title with no box:

| Written as | Printed (`lang: ja`) |
|---|---|
| `::: {.proof}` | *証明.* |
| `::: {#rem-…}` or `::: {.remark}` | *注釈 1.1.* |
| `::: {#sol-…}` or `::: {.solution}` | *解答.* |

They look nothing like the boxed exercise they usually follow. That is Quarto's
default, not a bug — but keep it in mind when writing an exercise/solution pair.

---

## 3. Callouts

Five types, no others. `.callout-info` **does not exist** — it degrades to a
typeless box whose screen-reader label is literally "None".

| Type | Prefix (when referenced) | Printed (`lang: ja`) | Use for |
|---|---|---|---|
| `note` | `#nte-` | ノート | a clarification or aside in the argument |
| `tip` | `#tip-` | ヒント | practical how-to, something to try at the keyboard |
| `warning` | `#wrn-` | 警告 | a common mistake |
| `important` | `#imp-` | 重要 | something easy to miss with real consequences |
| `caution` | `#cau-` | 注意 | a step that is hard to undo |

**Icons are off in every book**, set once as `callout-icon: false` in the
extension, in HTML and PDF alike. Writing `icon=false` on a block is redundant —
leave it out. Callout text is body-sized, not Quarto's default `.9rem`.

**Every callout gets a title.** An untitled callout renders as a box labelled
just ノート — it tells the student to stop, then doesn't say why. Give it a
title as a leading heading, or with `title=`:

```markdown
::: {.callout-note}
### なぜ指数分布は $M$ と書くのか
…
:::
```

### Referenceable callouts

A callout is cross-referenceable when it has **both** an `#<prefix>-` id **and**
a title. The id comes first, the class second:

```markdown
::: {#tip-sqlite-install .callout-tip}
## SQLite のインストール
…
:::

詳しくは @tip-sqlite-install を参照．
```

Without a title the reference will not resolve.

### Syntax that silently fails

Never write these. All three were live bugs in these books:

| Wrong | Renders as | Right |
|---|---|---|
| `:::{note}` | `<div class="{note}">` — an unstyled div | `:::{.callout-note}` |
| `::: {.callout .callout-info}` | typeless box, screen-reader label "None" | `::: {.callout-note}` |
| `:::{$exm-foo}` | unstyled div, never numbered | `:::{#exm-foo}` |

The braces need a `.` for a class and a `#` for an id. A bare word is neither.

---

## 4. Cross-references in Japanese books

Theorem-type references localize. **Callout and remark references do not** —
this is a Quarto limitation, not a configuration mistake:

```
@def-relation  →  定義 1.1      ✅
@nte-history   →  Note 1.1      ❌ English, in a Japanese sentence
@rem-caveat    →  Remark 1.1    ❌
```

Quarto's `_language-ja.yml` defines `callout-note-title: "ノート"` for the box
header, but has no `crossref-nte-title`, so the inline reference falls back to
English. Neither `crossref: nte-title:` nor `language: crossref-nte-title:` is
accepted.

**This is accepted, not a bug to fix.** Callouts are skippable by definition
(§1), so they are rarely cited — and the same goes for `#alg-` and `#rem-`.
An English label in a handful of references is not worth extra configuration
in every book. The rule that follows from this is the one below: reference
theorem-type blocks, not callouts.

A working fix exists should that ever change. Verified, but **deliberately not
applied** — add to a Japanese book's `_quarto.yml`:

```yaml
crossref:
  custom:
    - {key: nte, kind: float, reference-prefix: "ノート"}
    - {key: tip, kind: float, reference-prefix: "ヒント"}
    - {key: wrn, kind: float, reference-prefix: "警告"}
    - {key: imp, kind: float, reference-prefix: "重要"}
    - {key: cau, kind: float, reference-prefix: "注意"}
```

Callouts keep rendering as callouts; only the inline label changes.

> **Do not add `rem` to that list.** It converts remarks into figure-style
> floats. `@rem-` stays English; prefer a theorem-type block if you need to
> reference it.

Because of this, in Japanese chapters **prefer a theorem-type block for
anything you intend to reference**, and give callouts an id only when you
actually link to them.

---

## 5. Punctuation in Japanese books

Japanese chapters use **`，` (U+FF0C) and `．` (U+FF0E)** — never `、` and `。`.

| Wrong | Right |
|---|---|
| リレーション $R$ とは、部分集合である。 | リレーション $R$ とは，部分集合である． |

This is the horizontal-writing style of Japanese scientific and technical
writing, and it suits books this mathematical: `，．` are the same marks already
used inside the formulas, so a sentence that runs from prose into math keeps one
punctuation style throughout.

The rule covers the whole `.qmd` source — prose, headings, callout and
environment titles, and Japanese written inside code and comments. Two things
keep their original punctuation:

- **Verbatim quotations** from an external source.
- **Anything that must match what actually runs** — a string a program prints,
  or data reproduced from a file.

Convert **a whole file at a time**. Consistency within a chapter matters more
than consistency across the shelf, and a half-converted file reads worse than
either style alone.

`or-book` is the reference: 39 chapters, zero `、` or `。`. Not applicable to
`rl-book`, which is `lang: en`.

The linter checks this, one warning per file, in books whose `_quarto.yml` says
`lang: ja`. It reads prose only — fenced code, inline code spans and `「…」`
quotations are skipped, so the two exceptions above never get flagged, and
Japanese punctuation inside code is yours to keep consistent by eye.

---

## 6. House rules

1. **Every callout has a title.**
2. **学習目標 is `## 学習目標`**, never a callout — objectives belong in the TOC.
3. When chapter prose follows the objectives, give it its own section. The
   house pattern is `## 〜とは` (`## 待ち行列とは`, `## 機械語とは`,
   `## 擬似コードとは`).
4. **Ids are lowercase, hyphen-separated, and topical**: `#exm-serial-basic`,
   not `#exm-1`. Numbers renumber themselves; ids should survive reordering.
   Ids must be **unique across the whole book**, not just within a file —
   Quarto will not warn you about a collision.
5. **`note` vs `tip`**: `note` clarifies the argument, `tip` tells the reader
   what to do at the keyboard. Pick one meaning and hold it.
6. **Never** `:::{note}`, `.callout-info`, or a bare word in braces.
7. Solutions use `#sol-`; keep them adjacent to the `#exr-` they answer.
8. **Japanese books punctuate with `，．`**, never `、。` (§5).

---

## 7. How the theme colours these

From `_extensions/lecture/theme.scss` — the accent tells the reader the kind of
block at a glance:

| Block | Accent (light / dark) |
|---|---|
| `#exm-` example | teal `#137a72` / `#4bbfae` |
| `#exr-` exercise | amber `#b06e00` / `#d9a441` |
| `#thm-` `#lem-` `#cor-` `#prp-` `#def-` … | indigo `#2c5f8a` / `#6fa8dc` |
| callouts | Quarto's own per-type colours |

Change these in `_brand.yml`, never in a book.

---

## 8. Current usage

Where the five books stand today, as a baseline to improve on:

| | count |
|---|---|
| `#exm-` | 148 |
| `#exr-` | 80 |
| `#def-` | 38 |
| `#sol-` | 35 |
| `#thm-` / `#alg-` / `#lem-` / `#prp-` / `#rem-` | 8 / 6 / 5 / 3 / 1 |
| callouts (`note` 73, `tip` 24) | 97 |
| **of which still untitled** | **76** |
| Japanese chapters whose prose still uses `、` or `。` | **55 of 154** |

Three things visible in that table. Titling the 76 untitled callouts is the
highest-value cleanup available. `#thm-` at 8 against `#def-` at 38 is low for
books this mathematical — some results currently written as prose or as
`callout-note` should be `#thm-` or `#prp-` so they can be referenced. And 55
chapters still punctuate with `、。`, every one of them outside `or-book` (§5).

Run `python3 scripts/lint-conventions.py ~/Github` to check the rules that can
be checked mechanically.
