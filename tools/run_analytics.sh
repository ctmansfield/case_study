PYBIN=${PYBIN:-.venv_case/bin/python}
if [ ! -x "$PYBIN" ]; then PYBIN=$(command -v python3); fi
#!/usr/bin/env bash
# fail-soft runner (no set -e), prints where outputs went
python3 tools/analyze_bp_hr.py    || echo "[warn] bp/hr analysis failed"
python3 tools/analyze_glucose.py  || echo "[warn] glucose analysis failed"
python3 tools/analyze_sleep.py    || echo "[warn] sleep analysis failed"
python3 tools/analyze_med_response.py || echo "[warn] med response analysis failed"

echo
echo "→ analytics written under data/analytics/"
echo "→ plots written under data/plots/"
