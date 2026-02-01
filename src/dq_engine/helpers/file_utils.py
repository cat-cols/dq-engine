# Help find a file in multiple directories
    # Why:
    # Many later sections will need “search these known roots for a filename.”
    # Centralizing prevents copy paste drift.
    # Naming:
    # If you intend other modules to use it, drop the underscore: find_file_in_dirs.
    # If it is internal notebook glue only, keep _find_file_in_dirs.
    # Also make it consistent with your project roots.

from pathlib import Path

# find file in candidate dirs
def find_file_in_dirs(fname, dirs):
    """
    Search for a file `fname` in a list of directories `dirs`.
    Returns the first Path where the file exists, or None if not found.
    """
    for d in dirs:
        p = Path(d) / fname
        if p.exists():
            return p
    p = Path.cwd() / fname
    return p if p.exists() else None

# find file in candidate dirs
if "_find_file_in_dirs" not in globals():
    def _find_file_in_dirs(fname, dirs):
        for d in dirs:
            if d is None:
                continue
            p = Path(d) / fname
            if p.exists():
                return p
        p = Path.cwd() / fname
        if p.exists():
            return p
        return None

# def _find_file_in_dirs(fname, dirs):
#     """Return first existing Path for fname in given dirs, else None."""
#     for d in dirs:
#         if d is None:
#             continue
#         p = Path(d) / fname
#         if p.exists():
#             return p
#     # also check CWD as absolute fallback
#     p = Path.cwd() / fname
#     if p.exists():
#         return p
#     return None


# def _find_file_in_dirs(fname, dirs):
#     """Return first existing Path for fname in given dirs, else None."""
#     for d in dirs:
#         if d is None:
#             continue
#         p = Path(d) / fname
#         if p.exists():
#             return p
#     p = Path.cwd() / fname
#     if p.exists():
#         return p
#     return None
