#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ -x "$ROOT_DIR/.venv/bin/python" ]; then
  PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
elif [ -x "$ROOT_DIR/.venv/Scripts/python.exe" ]; then
  PYTHON_BIN="$ROOT_DIR/.venv/Scripts/python.exe"
else
  PYTHON_BIN="${PYTHON:-python3}"
  if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    if command -v python >/dev/null 2>&1; then
      PYTHON_BIN="python"
    else
      echo "Error: Python was not found in PATH." >&2
      exit 1
    fi
  fi
fi

"$PYTHON_BIN" -m pip install --quiet -e ".[build]"

rm -rf dist build *.spec
"$PYTHON_BIN" -m PyInstaller --clean --onefile \
  --name quantum-cli \
  --collect-all qiskit \
  --collect-all qiskit_aer \
  src/quantum_cli/__main__.py

echo "Build successful."
echo "Executable:"
ls -l dist
