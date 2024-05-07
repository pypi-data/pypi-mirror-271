# 2024 Steven Goncalo
from importlib.metadata import version
from logging import getLevelName

"""
Logging utilities provides a few helpful static methods.
"""
def libsrg_version():
    """Return the version of the libsrg package."""
    ver = version('libsrg')
    return f"libsrg {ver} {__file__} "


def level2str(lev) -> str:
    """Convert a level to a string."""
    if not isinstance(lev, str):
        lev = getLevelName(lev)
    return lev


def level2int(lev) -> int:
    """Convert a level to a number."""
    if isinstance(lev, str):
        lev = getLevelName(lev)
    return lev
