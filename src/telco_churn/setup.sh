Introduce basic setup script

!/usr/bin/env bash
Level 3 setup script — minimal, disciplined environment bootstrap
Usage: run from your project root (e.g., /Users/b/DATA/PROJECTS/Telco/Level_3)
  bash setup_env.sh

set -euo pipefail

ENV_NAME=".venv"
REQ_FILE="requirements.txt"

echo "📁 Project: $(pwd)"

# 1) Create venv if missing
if [[ ! -d "$ENV_NAME" ]]; then
  echo "🧪 Creating virtual environment ($ENV_NAME)…"
  python3 -m venv "$ENV_NAME"
else
  echo "🧪 Virtual environment already exists ($ENV_NAME)."
fi

# 2) Activate venv
# shellcheck disable=SC1091
source "$ENV_NAME/bin/activate"
echo "✅ Activated: $VIRTUAL_ENV"

# 3) Upgrade pip (cleaner dependency resolution)
echo "⬆️  Upgrading pip…"
python -m pip install --upgrade pip

# 4) Install dependencies
if [[ -f "$REQ_FILE" ]]; then
  echo "📦 Installing from $REQ_FILE…"
  pip install -r "$REQ_FILE"
else
  echo "📦 No $REQ_FILE found — installing a minimal data stack and creating one."
  pip install jupyter pandas numpy matplotlib seaborn scikit-learn
  echo "🧷 Freezing versions → $REQ_FILE"
  pip freeze > "$REQ_FILE"
fi

# 5) Done
cat <<MSG

🎉 Environment ready.
👉 Next steps:
   source $ENV_NAME/bin/activate
   jupyter lab

💡 Tip: To make this env available in Jupyter's kernel list later:
   python -m ipykernel install --user --name=telco_level3 --display-name "Telco Level 3"
MSG
```

* a clean **Level 3 `setup_env.sh`** into the canvas—exactly the basics: `python -m venv`, upgrade `pip`, install from `requirements.txt` (or create one), and that’s it. Want me to also add a tiny `Makefile` with `make setup`, `make clean`, and `make lab` targets?