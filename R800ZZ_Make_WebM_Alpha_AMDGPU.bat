@echo off
cd /d "%~dp0"
if "%~1"=="" (
    echo Drop a video file onto this BAT file.
    pause
    exit /b 1
)
if not exist ".venv_amd\Scripts\python.exe" (
    echo ERROR: Run install_python_packages_AMD.bat first.
    pause
    exit /b 1
)
".venv_amd\Scripts\python.exe" r800zz_rvm_video.py "%~1" --mode alpha --output-dir "%~dp0." --crf 20 --device directml
pause
