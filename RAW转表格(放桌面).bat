@echo off
set "WORK=C:/Users/31479/WorkBuddy/2026-05-31-19-34-37"
set "PY=C:/Users/31479/.workbuddy/binaries/python/envs/default/Scripts/python.exe"

if "%~1"=="" (
    echo Bruker RAW to 2theta + Rel.Int Table
    echo Drag .raw file onto this icon.
    pause
    exit /b
)
if not exist "%PY%" set "PY=C:/ProgramData/Miniconda3/python.exe"

"%PY%" "%WORK%\raw_to_table.py" "%~1"
pause
