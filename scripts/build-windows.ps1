$ErrorActionPreference = 'Stop'

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

if (Test-Path "$RootDir\.venv\Scripts\python.exe") {
    $PythonBin = "$RootDir\.venv\Scripts\python.exe"
} elseif (Test-Path "$RootDir\.venv\bin\python") {
    $PythonBin = "$RootDir\.venv\bin\python"
} else {
    $PythonBin = "python"
}

& $PythonBin -m pip install --quiet -e ".[build]"

Remove-Item -Recurse -Force dist, build -ErrorAction SilentlyContinue
Remove-Item -Force *.spec -ErrorAction SilentlyContinue

& $PythonBin -m PyInstaller --clean --onefile --name quantum-cli --collect-all qiskit --collect-all qiskit_aer .\src\quantum_cli\__main__.py

Write-Host "Build successful."
Write-Host "Executable: dist/quantum-cli.exe"
