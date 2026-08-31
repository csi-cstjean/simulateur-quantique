# Build instructions

## Environnement virtuel

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Tests

```bash
pytest
```

## Exécution

```bash
python -m quantum_cli
```

## Build Linux

```bash
chmod +x scripts/build-linux.sh
./scripts/build-linux.sh
```

## Build Windows

Sur Windows PowerShell :

```powershell
./scripts/build-windows.ps1
```

## PyInstaller

Les scripts utilisent PyInstaller avec le mode --onefile et collectent les ressources Qiskit/Aer nécessaires au runtime.

```bash
python -m PyInstaller --clean --onefile --name quantum-cli --collect-all qiskit --collect-all qiskit_aer src/quantum_cli/__main__.py
```

### Résultat attendu

- Linux : dist/quantum-cli
- Windows : dist/quantum-cli.exe
