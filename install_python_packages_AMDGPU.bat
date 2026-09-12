@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ==========================================
echo R800ZZ RVM Tool - AMD GPU / DirectML Setup
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

powershell -NoProfile -Command "$g = Get-CimInstance Win32_VideoController | Where-Object { $_.Name -match 'AMD|Radeon' }; if ($g) { exit 0 } else { exit 1 }"
if errorlevel 1 (
    echo ERROR: No AMD/Radeon GPU was detected.
    pause
    exit /b 1
)

if not exist ".venv_amd\Scripts\python.exe" (
    echo Creating isolated AMD DirectML environment...
    python -m venv ".venv_amd"
    if errorlevel 1 goto :error
)

".venv_amd\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :error

rem torch-directml installs a compatible PyTorch and torchvision version.
".venv_amd\Scripts\python.exe" -m pip install --upgrade numpy torch-directml
if errorlevel 1 goto :error

echo.
echo Verifying DirectML...
".venv_amd\Scripts\python.exe" -c "import torch,torch_directml; d=torch_directml.device(); a=torch.tensor([1.0],device=d); b=(a+a).cpu().item(); print('PyTorch:',torch.__version__); print('DirectML device:',d); print('DirectML test:',b)"
if errorlevel 1 goto :error

echo.
echo AMD DirectML setup completed successfully.
pause
exit /b 0

:error
echo.
echo ERROR: AMD DirectML setup failed.
pause
exit /b 1
