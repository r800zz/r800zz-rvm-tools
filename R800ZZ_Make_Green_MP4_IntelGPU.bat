@echo off
cd /d "%~dp0"
if "%~1"=="" (
    echo Drop a video file onto this BAT file.
    pause
    exit /b 1
)
if not exist ".venv_intel\Scripts\python.exe" (
    echo ERROR: Run install_python_packages_Intel.bat first.
    pause
    exit /b 1
)
".venv_intel\Scripts\python.exe" r800zz_rvm_video.py "%~1" --mode green --output-dir "%~dp0." --crf 20 --device intel
pause
