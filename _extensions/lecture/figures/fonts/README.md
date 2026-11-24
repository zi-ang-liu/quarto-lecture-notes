# Figure fonts

The faces of the page, for matplotlib: Inter (Latin, digits) and Noto Sans JP
(kana, kanji), each at 400 and 600. `../sitecustomize.py` hands them to
matplotlib in every chapter Quarto executes; nothing is installed.

Made by `scripts/build-figure-fonts.py` in zi-ang-liu/quarto-lecture-notes
from the variable fonts in github.com/google/fonts (`ofl/inter`,
`ofl/notosansjp`): static instances (Inter at opsz 14, the instance the page
uses), hinting removed, and Noto Sans JP cut down to JIS X 0208 plus the
kana and symbol blocks. Both are under the SIL Open Font License 1.1; the
licences are beside them. These modified fonts keep their names, which
contain no Reserved Font Name.
