# Glossary builder for a Jupyter notebook
# - Extracts text from markdown + top-of-cell comments/docstrings
# - Ranks terms by (POS-filtered) frequency
# - Looks up definitions via NLTK WordNet
# - Writes glossary JSON to disk

# ---------- config (tweak as you like) ----------
NOTEBOOK_PATH = Path("")     # ← your notebook path
OUT_JSON      = Path("outputs/notebook_glossary.json")
TOP_K         = 150                       # max number of terms to keep
MIN_FREQ      = 2                         # keep terms that appear ≥ this many times
ALLOW_POS     = {"NN","NNS","NNP","NNPS","JJ","JJR","JJS"}  # nouns + adjectives
MIN_LEN       = 3                         # min token length (characters)
# -----------------------------------------------


import json, re, sys, os
from pathlib import Path
from collections import Counter, defaultdict

import nltk
# Auto-download lightweight models if missing
for pkg in ["punkt", "averaged_perceptron_tagger", "wordnet", "omw-1.4"]:
    try:
        nltk.data.find(f"tokenizers/{pkg}") if pkg=="punkt" else nltk.data.find(f"corpora/{pkg}")
    except LookupError:
        nltk.download(pkg, quiet=True)

from nltk.corpus import wordnet as wn
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer


def _extract_text_from_notebook(nb_path: Path) -> str:
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    texts = []

    for cell in nb.get("cells", []):
        ctype = cell.get("cell_type")
        src   = "".join(cell.get("source", []))

        if ctype == "markdown":
            texts.append(src)

        elif ctype == "code":
            # Top-of-cell comments (lines that START with '#')
            top_comments = []
            for line in src.splitlines():
                if line.strip().startswith("#"):
                    # stop once we hit the first non-comment/non-blank line
                    top_comments.append(re.sub(r"^#+\s?", "", line.strip()))
                elif line.strip() == "":
                    # still allow leading blanks
                    continue
                else:
                    break
            if top_comments:
                texts.append("\n".join(top_comments))

            # Top docstring (first triple-quoted block at cell start)
            m = re.match(r'\s*(("""|\'\'\'))(.*?)(\1)', src, flags=re.DOTALL)
            if m:
                doc = m.group(3)
                texts.append(doc)

    return "\n\n".join(texts)

def _normalize_tokens(text: str):
    # basic cleanup → tokens → POS tag → filter
    # keep simple hyphenated words; drop code-ish artifacts
    text = re.sub(r"[`*_<>]+", " ", text)
    text = re.sub(r"[\u2000-\u206F]", " ", text)  # misc punctuation range
    toks  = [t for t in word_tokenize(text) if re.search(r"[A-Za-z]", t)]
    tagged = pos_tag(toks)

    # map POS for lemmatization
    def to_wnpos(tag):
        return "n" if tag.startswith("NN") else ("a" if tag.startswith("JJ") else None)

    lem = WordNetLemmatizer()
    terms = []
    for tok, tag in tagged:
        if tag not in ALLOW_POS: 
            continue
        tok_clean = re.sub(r"[^A-Za-z\-]", "", tok).lower()
        if len(tok_clean) < MIN_LEN:
            continue
        wnpos = to_wnpos(tag)
        tok_lem = lem.lemmatize(tok_clean, wnpos) if wnpos else tok_clean
        terms.append(tok_lem)

    return terms

def _top_terms(terms, top_k=TOP_K, min_freq=MIN_FREQ):
    freq = Counter(terms)
    # simple priority: frequency, then alphabetical
    items = [(t, c) for t, c in freq.items() if c >= min_freq]
    items.sort(key=lambda x: (-x[1], x[0]))
    return [t for t, _ in items[:top_k]]

def _define_term(term: str) -> str:
    # get first sensible WordNet definition; fallbacks if none
    syns = wn.synsets(term)
    if not syns:
        return "(definition not found in WordNet)"
    # Prefer noun senses first, then adjective
    noun_first = [s for s in syns if s.pos() == 'n'] + [s for s in syns if s.pos() == 'a'] + syns
    return noun_first[0].definition()

def build_notebook_glossary(nb_path: Path, out_json: Path):
    text = _extract_text_from_notebook(nb_path)
    if not text.strip():
        raise ValueError("No extractable text found in the notebook.")

    terms = _normalize_tokens(text)
    keep  = _top_terms(terms, TOP_K, MIN_FREQ)

    glossary = {}
    for term in keep:
        try:
            glossary[term] = _define_term(term)
        except Exception:
            glossary[term] = "(definition lookup error)"

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(glossary, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"✅ Glossary built: {len(glossary)} terms")
    print(f"💾 Saved → {out_json}")
    # quick peek
    for i, (k, v) in enumerate(list(glossary.items())[:15], 1):
        print(f"{i:>2}. {k}: {v}")

# --- run ---
if __name__ == "__main__":
    try:
        build_notebook_glossary(NOTEBOOK_PATH, OUT_JSON)
    except Exception as e:
        print("⚠️ Failed to build glossary:", e)
