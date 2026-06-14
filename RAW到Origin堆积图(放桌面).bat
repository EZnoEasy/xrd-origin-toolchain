@echo off
setlocal enabledelayedexpansion
set "WORK=C:/Users/31479/WorkBuddy/2026-05-31-19-34-37"
set "PY=C:/ProgramData/Miniconda3/python.exe"

if "%~1"=="" (
    echo Bruker RAW to Origin XRD Stack Plot
    echo Drag .raw file(s) onto this icon.
    pause
    exit /b
)

set FILES=
for %%f in (%*) do set FILES=!FILES! "%%~f"

"%PY%" "%WORK%\raw_to_origin.py" !FILES!
pause
