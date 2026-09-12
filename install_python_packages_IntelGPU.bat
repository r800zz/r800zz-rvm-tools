@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ==========================================
echo R800ZZ RVM Tool - Intel GPU / DirectML Setup
echo ==========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python was not found.
    pause
    exit /b 1
)

echo Detected display adapters:
powershell -NoProfile -Command "Get-CimInstance Win32_VideoController | ForEach-Object { Write-Host ('  ' + $_.Name) }"
echo.

powershell -NoProfile -Command "$g = Get-CimInstance Win32_VideoController | Where-Object { $_.Name -match 'Intel' }; if ($g) { exit 0 } else { exit 1 }"
if errorlevel 1 (
    echo ERROR: No Intel GPU was detected.
    pause
    exit /b 1
)

if not exist ".venv_intel\Scripts\python.exe" (
    echo Creating isolated Intel DirectML environment...
    python -m venv ".venv_intel"
    if errorlevel 1 goto :error
)

".venv_intel\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :error

rem torch-directml installs a compatible PyTorch version.
".venv_intel\Scripts\python.exe" -m pip install --upgrade numpy torch-directml
if errorlevel 1 goto :error

echo.
echo Verifying Intel DirectML adapter...
".venv_intel\Scripts\python.exe" -c "import torch,torch_directml,sys; xs=[(i,torch_directml.device_name(i)) for i in range(torch_directml.device_count())]; print('DirectML adapters:',xs); m=[x for x in xs if 'intel' in x[1].lower()]; sys.exit(0 if m else 1)"
if errorlevel 1 goto :error

echo.
echo Intel DirectML setup completed successfully.
pause
exit /b 0

:error
echo.
echo ERROR: Intel DirectML setup failed.
pause
exit /b 1
