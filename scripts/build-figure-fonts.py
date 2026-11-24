#!/usr/bin/env python3
"""Build the fonts that figures are set in, into
_extensions/lecture/figures/fonts/.

The page sets its text in Inter and Noto Sans JP, served by Google Fonts. A
figure drawn by a code cell is set by matplotlib, which needs font files on
disk: these are made from the same variable fonts Google Fonts serves,

    https://github.com/google/fonts/blob/main/ofl/inter/Inter[opsz,wght].ttf
    https://github.com/google/fonts/blob/main/ofl/notosansjp/NotoSansJP[wght].ttf

plus the OFL.txt beside each. Download those four files into one folder,
keeping the ofl/<family>/ layout or not, and run

    /opt/miniconda3/envs/quarto-book/bin/python scripts/build-figure-fonts.py <folder>

(any Python with fontTools works; matplotlib depends on it.) It writes:

    Inter-Regular.ttf, Inter-SemiBold.ttf       opsz 14, the instance the page
                                                uses; weights 400 and 600
    NotoSansJP-Regular.ttf, -SemiBold.ttf       weights 400 and 600, cut down
                                                to JIS X 0208 (levels 1 and
                                                2), the four Joyo kanji outside
                                                it, kana and the symbol blocks
                                                Japanese text uses — 2.6 MB a
                                                weight instead of 5.4
    OFL-Inter.txt, OFL-NotoSansJP.txt           the licences, which have to
                                                travel with the fonts

Two weights, because a figure has two: text, and titles (600, like the
page's h2 and below). Hinting is dropped: matplotlib renders with FreeType's
autohinter and ignores a font's own instructions.
"""
import pathlib
import shutil
import sys

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

OUT = pathlib.Path(__file__).resolve().parent.parent / "_extensions/lecture/figures/fonts"
WEIGHTS = {400: "Regular", 600: "SemiBold"}


def japanese_text():
    """Every character a figure's Japanese text should need."""
    chars = set()
    for hi in range(0xA1, 0xFF):              # JIS X 0208, by way of EUC-JP
        for lo in range(0xA1, 0xFF):
            try:
                chars.add(bytes([hi, lo]).decode("euc_jp"))
            except UnicodeDecodeError:
                pass
    chars |= {"\U00020B9F", "塡", "剝", "頰"}   # 𠮟 塡 剝 頰
    for a, b in [(0x20, 0x7E), (0xA0, 0xFF), (0x370, 0x3FF), (0x2000, 0x206F),
                 (0x2070, 0x209F), (0x20A0, 0x20CF), (0x2100, 0x218F),
                 (0x2190, 0x23FF), (0x2460, 0x24FF), (0x2500, 0x257F),
                 (0x25A0, 0x27BF), (0x3000, 0x30FF), (0x31F0, 0x31FF),
                 (0x3200, 0x33FF), (0xFF00, 0xFFEF)]:
        chars |= {chr(c) for c in range(a, b + 1)}
    return "".join(sorted(chars))


def build(vf_path, axes, name, text=None):
    for wght, style in WEIGHTS.items():
        font = instancer.instantiateVariableFont(
            TTFont(vf_path), {**axes, "wght": wght}, updateFontNames=True)
        options = subset.Options()
        options.hinting = False
        options.name_IDs = ["*"]
        options.name_languages = ["*"]
        options.notdef_outline = True
        options.glyph_names = False
        sub = subset.Subsetter(options)
        if text is None:
            sub.populate(unicodes=font.getBestCmap().keys())
        else:
            sub.populate(text=text)
        sub.subset(font)
        out = OUT / f"{name}-{style}.ttf"
        font.save(out)
        print(f"{out.name:28s} {out.stat().st_size / 1e6:5.2f} MB")


def find(folder, pattern):
    hits = sorted(folder.rglob(pattern))
    if len(hits) != 1:
        sys.exit(f"expected one {pattern} under {folder}, found {len(hits)}")
    return hits[0]


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = pathlib.Path(sys.argv[1])
    OUT.mkdir(parents=True, exist_ok=True)
    inter = find(src, "Inter[[]opsz,wght[]].ttf")
    noto = find(src, "NotoSansJP[[]wght[]].ttf")
    build(inter, {"opsz": 14}, "Inter")
    build(noto, {}, "NotoSansJP", text=japanese_text())
    shutil.copyfile(inter.parent / "OFL.txt", OUT / "OFL-Inter.txt")
    shutil.copyfile(noto.parent / "OFL.txt", OUT / "OFL-NotoSansJP.txt")


if __name__ == "__main__":
    main()
