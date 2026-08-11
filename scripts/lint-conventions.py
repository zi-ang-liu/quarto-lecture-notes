#!/usr/bin/env python3
"""Check the lecture-note books against CONVENTION.md.

    python3 scripts/lint-conventions.py ~/Github

Only the rules that can be checked mechanically. Everything reported here is
either a silent rendering failure or a rule from CONVENTION.md section 5.
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


def check(path: pathlib.Path, rel: str):
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

    return [(rel, n, level, msg) for n, level, msg in out]


def main() -> int:
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").expanduser()
    findings = []
    for name in BOOKS:
        book = root / name
        if not book.is_dir():
            continue
        for path in chapters(book):
            findings += check(path, f"{name}/{path.relative_to(book)}")

    errors = [f for f in findings if f[2] == "ERROR"]
    for rel, n, level, msg in sorted(findings, key=lambda f: (f[2] != "ERROR", f[0], f[1])):
        print(f"{level:5} {rel}:{n}  {msg}")

    print(f"\n{len(errors)} error(s), {len(findings) - len(errors)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
