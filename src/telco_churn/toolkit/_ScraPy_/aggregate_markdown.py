# a **utility script** that extracts all **Markdown cell text** from a Jupyter notebook (`.ipynb`) and saves it into a new text/Markdown file (for documentation or README generation).
# - clean, production-grade version:
# * Read all Markdown cells from your notebook.
# * Combine them (with `---` dividers between sections).
# * Output a single Markdown file (`Telco_Level3_Docs.md`) ready for use in your `docs/` or `README` folder.


# 🪄 Example usage
# python extract_markdown_cells.py Telco_Level3_Notebook.ipynb Telco_Level3_Docs.md

### 🧠 Optional Enhancements
# You can easily extend it to:
# * Include code cell comments (`cell_type == 'code'` and lines starting with `#`).
# * Prepend section headers (`# Cell N`) for better navigation.
# * Save to your **project’s docs directory** automatically:

#   ```python
#  output_path = Path("docs") / (input_path.stem + "_mdcells.md")
#   ```

### 🧰 `extract_markdown_cells.py` script:

#!/usr/bin/env python3
"""
Extract all Markdown cell text from a Jupyter Notebook
and save it as a single Markdown file.

Usage:
    python extract_markdown_cells.py notebook.ipynb output.md
"""

import json
from pathlib import Path
import sys

def extract_markdown_cells(input_path: Path, output_path: Path):
    """Aggregate markdown cell text from a Jupyter notebook into one .md file."""
    if not input_path.exists():
        raise FileNotFoundError(f"❌ Notebook not found: {input_path}")
    if input_path.suffix != ".ipynb":
        raise ValueError("❌ Input must be a .ipynb file")

    with input_path.open("r", encoding="utf-8") as f:
        nb = json.load(f)

    # Collect all markdown cell sources
    md_cells = []
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "markdown":
            text = "".join(cell.get("source", []))
            md_cells.append(text.strip())

    if not md_cells:
        print("⚠️ No markdown cells found.")
        return

    # Join with clear separators
    combined = "\n\n---\n\n".join(md_cells)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        f.write(combined)

    print(f"✅ Extracted {len(md_cells)} markdown cells → {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_markdown_cells.py notebook.ipynb output.md")
        sys.exit(1)
    extract_markdown_cells(Path(sys.argv[1]), Path(sys.argv[2]))


# TODO: extend it so it:
# *also captures top-of-cell comments* (like `# 2.1 Missing / Null / Blank Scan`)?


# Got it—here’s a **no-function** version that aggregates:

# * All **Markdown cells**, and
# * The **top-of-cell comments** from **code cells** (lines starting with `#` at the very top, before any code), and
# * (Optional) a **top triple-quoted docstring** if it’s the first thing in a code cell.

# It outputs a single `.md` file with `---` dividers.

# ```python
# #!/usr/bin/env python3
# # Extract markdown cells + top-of-cell comments (and optional top docstrings) into one .md
# # Usage:
# #   python extract_markdown_cells.py notebook.ipynb output.md

# import json
# from pathlib import Path
# import re
# import sys

# # --- Args / guards (no functions) ---
# if len(sys.argv) < 3:
#     print("Usage: python extract_markdown_cells.py notebook.ipynb output.md")
#     sys.exit(1)

# input_path = Path(sys.argv[1])
# output_path = Path(sys.argv[2])

# if not input_path.exists():
#     raise FileNotFoundError(f"❌ Notebook not found: {input_path}")
# if input_path.suffix != ".ipynb":
#     raise ValueError("❌ Input must be a .ipynb file")

# # --- Load notebook JSON ---
# nb = json.loads(input_path.read_text(encoding="utf-8"))

# # --- Helpers (inline) ---
# TRIPLE_START_RE = re.compile(r'^\s*(?:[rubfRUBF]{0,4})?([\'"]{3})')  # """ or '''
# def _strip_md_lines(text):
#     # Normalize cell markdown text
#     return text.replace('\r\n', '\n').strip()

# def _comment_block_from_code_source(lines):
#     """
#     Return (md_text, consumed_idx)
#     - Capture contiguous top '# ...' comment lines (ignoring blank lines in between if they are still part of the top).
#     - Optionally capture a top triple-quoted docstring block if it is the first non-blank thing.
#     """
#     i = 0
#     n = len(lines)
#     md_chunks = []

#     # Skip initial blank lines but remember if we pass something non-comment later
#     while i < n and lines[i].strip() == "":
#         i += 1

#     # 1) Hash-comment block at the very top
#     start_i = i
#     while i < n:
#         stripped = lines[i].lstrip()
#         if stripped.startswith("#"):
#             # Convert "# " → Markdown text; strip only one leading '#' and one space if present
#             line = stripped[1:]
#             if line.startswith(" "):
#                 line = line[1:]
#             md_chunks.append(line.rstrip())
#             i += 1
#             continue
#         elif stripped == "":  # allow blank lines inside the top comment block
#             md_chunks.append("")  # preserve spacing
#             i += 1
#             continue
#         else:
#             break

#     if md_chunks:
#         # If we captured any hash comments, return them (don’t also try to capture docstring)
#         md_text = "\n".join(md_chunks).strip()
#         return (md_text, i)

#     # 2) If no hash comments, consider a top triple-quoted docstring
#     i = start_i
#     if i < n:
#         m = TRIPLE_START_RE.match(lines[i])
#         if m:
#             quote = m.group(1)
#             doc_lines = [lines[i]]
#             i += 1
#             closed = False
#             while i < n:
#                 doc_lines.append(lines[i])
#                 if quote in lines[i]:
#                     closed = True
#                     i += 1
#                     break
#                 i += 1
#             if closed:
#                 # Turn the docstring into Markdown (strip the enclosing triple quotes)
#                 doc_text = "".join(doc_lines)
#                 # Remove the first and last triple-quote occurrence
#                 first = doc_text.find(quote)
#                 last = doc_text.rfind(quote)
#                 if first != -1 and last != -1 and last > first:
#                     md_text = doc_text[first+len(quote):last].strip()
#                     return (md_text, i)

#     # Nothing captured
#     return ("", start_i)

# # --- Aggregate ---
# aggregated = []
# cell_count = 0
# md_cell_count = 0
# comment_cell_count = 0

# for cell in nb.get("cells", []):
#     cell_count += 1
#     ctype = cell.get("cell_type")
#     src = cell.get("source", [])
#     # Source can be a list of lines or a single string
#     if isinstance(src, list):
#         lines = src
#     else:
#         lines = src.splitlines(True)  # keep line endings

#     if ctype == "markdown":
#         text = _strip_md_lines("".join(lines))
#         if text:
#             aggregated.append(text)
#             md_cell_count += 1

#     elif ctype == "code":
#         # Capture top-of-cell comment block (and maybe a top docstring)
#         md_text, _ = _comment_block_from_code_source(lines)
#         md_text = _strip_md_lines(md_text)
#         if md_text:
#             # If the first non-empty line looks like a heading (e.g., "2.1 ..."), add '## ' prefix for readability
#             first_line = md_text.splitlines()[0].strip()
#             if not first_line.startswith(("#", "##", "###")):
#                 md_text = "## " + first_line + ("\n" + "\n".join(md_text.splitlines()[1:]) if "\n" in md_text else "")
#             aggregated.append(md_text)
#             comment_cell_count += 1

# # --- Write output ---
# output_path.parent.mkdir(parents=True, exist_ok=True)
# if aggregated:
#     out_text = ("\n\n---\n\n").join(aggregated).rstrip() + "\n"
#     output_path.write_text(out_text, encoding="utf-8")
#     print(f"✅ Wrote {md_cell_count} markdown cells + {comment_cell_count} top-of-cell comment/docstring blocks "
#           f"(from {cell_count} cells) → {output_path}")
# else:
#     print("⚠️ No markdown or top-of-cell comments/docstrings found.")
# ```

# **What it captures:**

# * All Markdown cells (as-is).
# * For each code cell, it grabs the **contiguous top block of `#` comments** (allowing blank lines inside the block), converts them to Markdown text, and prefixes the first line with `## ` if you didn’t already use `#` in the comment.
# * If a code cell doesn’t start with `#` comments but **does** start with a **triple-quoted docstring** (`"""..."""` or `'''...'''`, with optional `r/u/b/f` prefixes), it captures that block instead.

# **Usage:**
# python extract_markdown_cells.py Level_3_Telco.ipynb Level_3_Telco_Markdown.md

