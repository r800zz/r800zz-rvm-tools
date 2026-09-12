@echo off
cd /d "%~dp0"
if "%~1"=="" (
    echo Drop a video file onto this BAT file.
    pause
    exit /b 1
)
python r800zz_rvm_video.py "%~1" --mode alpha --output-dir "%~dp0." --crf 20
pause
