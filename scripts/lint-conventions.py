#!/usr/bin/env python3
"""Check the lecture-note books against CONVENTION.md.

    python3 scripts/lint-conventions.py ~/Github

Only the rules that can be checked mechanically. Everything reported here is
either a silent rendering failure or a rule from CONVENTION.md section 6.
"""

import pathlib
import re
import sys

BOOKS = ["or-book", "rl-book", "data-science-book",
         "computer-literacy-book", "database-book"]

VALID_CALLOUTS = {"note", "tip", "warning", "important", "caution"}
THEOREM_PREFIXES = {"thm", "lem", "cor", "prp", "cnj", "def",
                    "exm", "exr", "alg", "sol", "rem"}
CALLOUT_PREFIXES = {"nte", "tip", "wrn", "imp", "cau"}


def chapters(book: pathlib.Path):
    """Only files actually listed in _quarto.yml — scratch files don't count."""
    cfg = book / "_quarto.yml"
    if not cfg.exists():
        return []
    listed = {ln.strip().lstrip("- ").strip()
              for ln in cfg.read_text(encoding="utf-8").splitlines()
              if ln.strip().lstrip("- ").endswith(".qmd")}
    return [book / rel for rel in sorted(listed) if (book / rel).exists()]


def is_japanese(book: pathlib.Path) -> bool:
    """§5 applies to the Japanese books only; rl-book is lang: en."""
    cfg = book / "_quarto.yml"
    return bool(cfg.exists() and re.search(
        r"^lang:\s*ja\b", cfg.read_text(encoding="utf-8"), re.M))


def prose_lines(text: str):
    """(lineno, line) for prose only — the parts §5 actually governs.

    Dropped: fenced code and inline code spans, because the linter cannot tell
    a string a program really prints from prose the author typed; and 「…」/『…』
    runs, which are quotations, UI labels, or the punctuation marks themselves
    under discussion (see computer-literacy-book's IME chapter).
    """
    fence = None
    for n, line in enumerate(text.splitlines(), 1):
        m = re.match(r"\s*(`{3,}|~{3,})", line)
        if m:
            mark = m.group(1)[0] * 3
            if fence is None:
                fence = mark
            elif fence == mark:
                fence = None
            continue
        if fence is None:
            yield n, re.sub(r"「[^」]*」|『[^』]*』", "",
                            re.sub(r"`[^`]*`", "", line))


def check(path: pathlib.Path, rel: str, ja: bool = False):
    text = path.read_text(encoding="utf-8", errors="replace")
    out = []

    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not s.startswith(":::"):
            continue
        m = re.match(r":::+\s*\{([^}]*)\}", s)
        if not m:
            continue
        attrs = m.group(1).strip()

        if attrs and not re.search(r"[.#]", attrs):
            out.append((n, "ERROR", f"bare word in braces — renders as an unstyled div: {s[:44]}"))
        if "$" in attrs:
            out.append((n, "ERROR", f"'$' in an attribute block — did you mean '#'? {s[:44]}"))
        for c in re.findall(r"\.callout-([a-z]+)", attrs):
            if c not in VALID_CALLOUTS:
                out.append((n, "ERROR", f"'{c}' is not a Quarto callout type"))
        for key in re.findall(r"#(\w+)-", attrs):
            if key not in THEOREM_PREFIXES | CALLOUT_PREFIXES:
                out.append((n, "WARN", f"unknown crossref prefix '#{key}-'"))

    # Untitled callouts, and referenceable ones missing the required title.
    for m in re.finditer(r"^::: *\{([^}]*callout-\w+[^}]*)\}\n(.*?)^:::", text,
                         re.S | re.M):
        attrs, body = m.group(1), m.group(2).strip()
        n = text[:m.start()].count("\n") + 1
        titled = "title=" in attrs or re.match(r"#{2,4} +\S", body)
        if not titled:
            ref = re.search(r"#(\w+)-", attrs)
            if ref:
                out.append((n, "ERROR", "referenceable callout has no title — @ref will not resolve"))
            else:
                out.append((n, "WARN", "callout has no title"))

    # 学習目標 must be a section heading, not a callout.
    if "学習目標" in text and not re.search(r"^## 学習目標", text, re.M):
        n = text[:text.index("学習目標")].count("\n") + 1
        out.append((n, "WARN", "学習目標 should be '## 学習目標', not a callout"))

    # 、。 in a Japanese book (§5). Reported once per file, at the first
    # offending line: the fix is to convert the whole file in one pass.
    if ja:
        hits = [n for n, line in prose_lines(text)
                if "、" in line or "。" in line]
        if hits:
            out.append((hits[0], "WARN",
                        f"{len(hits)} line(s) use 、 or 。 — Japanese books "
                        f"punctuate with ，． (§5)"))

    return [(rel, n, level, msg) for n, level, msg in out]


def duplicate_ids(book: pathlib.Path, name: str):
    """Crossref ids must be unique book-wide; Quarto does not warn on collisions."""
    seen = {}
    dups = []
    for path in chapters(book):
        rel = f"{name}/{path.relative_to(book)}"
        for n, line in enumerate(path.read_text(encoding="utf-8", errors="replace")
                                 .splitlines(), 1):
            if line.lstrip().startswith("<!--"):
                continue
            m = re.match(r"\s*:::+ *\{#([\w-]+)\}\s*$", line)
            if not m:
                continue
            key = m.group(1)
            if key in seen:
                dups.append((rel, n, "ERROR",
                             f"duplicate id '#{key}' — also at {seen[key]}"))
            else:
                seen[key] = f"{rel}:{n}"
    return dups


def main() -> int:
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").expanduser()
    findings = []
    for name in BOOKS:
        book = root / name
        if not book.is_dir():
            continue
        ja = is_japanese(book)
        for path in chapters(book):
            findings += check(path, f"{name}/{path.relative_to(book)}", ja)
        findings += duplicate_ids(book, name)

    errors = [f for f in findings if f[2] == "ERROR"]
    for rel, n, level, msg in sorted(findings, key=lambda f: (f[2] != "ERROR", f[0], f[1])):
        print(f"{level:5} {rel}:{n}  {msg}")

    print(f"\n{len(errors)} error(s), {len(findings) - len(errors)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
