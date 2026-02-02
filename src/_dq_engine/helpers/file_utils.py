
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
