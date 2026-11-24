"""Point matplotlib at the lecture style in every chapter Quarto executes.

A book's `_environment` puts this folder on PYTHONPATH, so Python imports this
module when it starts, in every kernel Quarto launches for that book. It only
sets an environment variable; matplotlib reads MATPLOTLIBRC itself when a
chapter imports it. A value already set (to try another style) wins.

Why not set MATPLOTLIBRC in `_environment` directly: a relative path there is
resolved against the chapter's folder, and Quarto does not expand the project
directory in that file. This module knows where it is, so the path it sets
is absolute.

Code run outside Quarto (a notebook, VS Code's interactive window) does not
come through here and draws with matplotlib's own defaults.
"""

import os

os.environ.setdefault(
    "MATPLOTLIBRC",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "matplotlibrc"),
)
