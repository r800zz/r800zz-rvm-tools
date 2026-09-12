@echo off
setlocal EnableExtensions
cd /d "%~dp0"

rem R800ZZ RVM Tool - PyTorch NVIDIA GPU setup
rem Current stable CUDA wheel channel used by this installer.
set "TORCH_INDEX=https://download.pytorch.org/whl/cu132"

echo ==========================================
echo R800ZZ RVM Tool - PyTorch GPU Setup
echo ==========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python was not found.
    pause
    exit /b 1
)

python -m pip install --upgrade pip
if errorlevel 1 goto :error

python -m pip install --upgrade numpy
if errorlevel 1 goto :error

rem Check whether PyTorch is already installed.
python -c "import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('torch') else 1)" >nul 2>&1
if errorlevel 1 goto :install_new

rem Check whether the installed PyTorch build has CUDA support.
python -c "import torch,sys; sys.exit(0 if torch.version.cuda is not None else 1)" >nul 2>&1
if errorlevel 1 goto :replace_cpu

echo GPU-enabled PyTorch is already installed.
echo Checking for a newer GPU-enabled version...
python -m pip install --upgrade torch torchvision --index-url "%TORCH_INDEX%"
if errorlevel 1 goto :error
goto :verify

:replace_cpu
echo CPU-only PyTorch was detected.
echo Replacing it with the latest GPU-enabled PyTorch...
python -m pip uninstall -y torch torchvision torchaudio
if errorlevel 1 goto :error
python -m pip install torch torchvision --index-url "%TORCH_INDEX%"
if errorlevel 1 goto :error
goto :verify

:install_new
echo PyTorch is not installed.
echo Installing the latest GPU-enabled PyTorch...
python -m pip install torch torchvision --index-url "%TORCH_INDEX%"
if errorlevel 1 goto :error

:verify
echo.
echo ==========================================
echo Installed PyTorch
echo ==========================================
python -c "import torch; print('PyTorch:', torch.__version__); print('PyTorch CUDA:', torch.version.cuda); print('CUDA available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NOT AVAILABLE')"
if errorlevel 1 goto :error

python -c "import torch,sys; sys.exit(0 if torch.version.cuda is not None else 1)" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: The installed PyTorch is still CPU-only.
    pause
    exit /b 1
)

python -c "import torch,sys; sys.exit(0 if torch.cuda.is_available() else 1)" >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: GPU-enabled PyTorch is installed, but CUDA is not currently available.
    echo Check the NVIDIA driver.
    pause
    exit /b 2
)

echo.
echo Setup completed successfully.
pause
exit /b 0

:error
echo.
echo ERROR: Setup failed.
pause
exit /b 1
