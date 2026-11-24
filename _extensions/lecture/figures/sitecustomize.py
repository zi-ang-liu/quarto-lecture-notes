"""Point matplotlib at the lecture style in every chapter Quarto executes.

A book's `_environment` puts this folder on PYTHONPATH, so Python imports this
module when it starts, in every kernel Quarto launches for that book. It does
two things, neither of which imports matplotlib — a chapter that never draws
pays nothing:

- It sets MATPLOTLIBRC to matplotlibrc beside it. matplotlib reads that
  variable itself when a chapter imports it. A value already set (to try
  another style) wins.
- It hands matplotlib the fonts in fonts/ (Inter and Noto Sans JP, the faces
  of the page) the moment matplotlib.font_manager is first imported. They
  are not installed anywhere, so the same figures come out on any machine.

Why not set MATPLOTLIBRC in `_environment` directly: a relative path there is
resolved against the chapter's folder, and Quarto does not expand the project
directory in that file. This module knows where it is, so the path it sets
is absolute.

Code run outside Quarto (a notebook, VS Code's interactive window) does not
come through here and draws with matplotlib's own defaults.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_FONTS = os.path.join(_HERE, "fonts")

os.environ.setdefault("MATPLOTLIBRC", os.path.join(_HERE, "matplotlibrc"))


class _AddLectureFonts:
    """An import hook that waits for matplotlib.font_manager.

    It finds the module the usual way, through the finders after it, and has
    the module's loader add the fonts once the module has run — before any
    chapter code can ask for a font. Everything else it lets pass.
    """

    def find_spec(self, name, path=None, target=None):
        if name != "matplotlib.font_manager":
            return None
        for finder in sys.meta_path:
            if finder is self or not hasattr(finder, "find_spec"):
                continue
            spec = finder.find_spec(name, path, target)
            if spec is not None:
                break
        else:
            return None
        loader = spec.loader
        if loader is None or not hasattr(loader, "exec_module"):
            return spec
        run = loader.exec_module

        def exec_module(module):
            run(module)
            try:
                for f in sorted(os.listdir(_FONTS)):
                    if f.endswith(".ttf"):
                        module.fontManager.addfont(os.path.join(_FONTS, f))
            except Exception:       # never stop a chapter over a font
                pass

        loader.exec_module = exec_module
        return spec


if os.path.isdir(_FONTS):
    sys.meta_path.insert(0, _AddLectureFonts())
