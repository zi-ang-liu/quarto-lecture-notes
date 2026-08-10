#!/usr/bin/env bash
# Pull the newest lecture-notes extension into every local book clone.
#
#   ./scripts/update-books.sh              # update only
#   ./scripts/update-books.sh --commit     # update, then commit the bump
#
# Run this after tagging a new version here, so each repo's committed
# _extensions match what CI deploys.

set -euo pipefail

BOOKS_DIR="${BOOKS_DIR:-$HOME/Github}"
EXTENSION="zi-ang-liu/quarto-lecture-notes"
BOOKS=(or-book rl-book data-science-book computer-literacy-book database-book)

commit=false
[[ "${1:-}" == "--commit" ]] && commit=true

for book in "${BOOKS[@]}"; do
  dir="$BOOKS_DIR/$book"

  if [[ ! -d "$dir/_extensions" ]]; then
    echo "skip $book (extension not installed yet — run: quarto add $EXTENSION)"
    continue
  fi

  echo "==> $book"
  (
    cd "$dir"
    quarto update "$EXTENSION" --no-prompt

    if $commit && ! git diff --quiet -- _extensions; then
      git add _extensions
      git commit -m "Update lecture-notes extension"
      echo "    committed (not pushed)"
    fi
  )
done

echo "done"
