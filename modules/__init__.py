"""
Automatically load installed Miror B.ot modules
"""
import os as _os


# Awkward as fuck
def __load_modules__():
    """
    Automatically load installed Miror B.ot modules
    """
    pkg_path = _os.path.realpath(__file__)
    pkg_path = _os.path.dirname(pkg_path)

    mb_mods = []
    _, dirnames, filenames = next(_os.walk(pkg_path))

    remove = ("__pycache__", "__init__.py")
    for key in remove:
        if key in dirnames:
            dirnames.pop(dirnames.index(key))
        if key in filenames:
            filenames.pop(filenames.index(key))

    mods = dirnames + filenames
    for path in mods:
        module_name = path.replace(".py", "")
        mb_mods.append(module_name)

    return mb_mods


__all__ = __load_modules__()

from . import *  # noqa
