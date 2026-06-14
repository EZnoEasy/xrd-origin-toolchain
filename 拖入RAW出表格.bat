@echo off
title RAW to Table

if "%~1"=="" (
    echo Bruker RAW to 2theta Table
    echo Drag .raw file onto this bat icon.
    echo Output: *_table.csv and *_table.xlsx in same folder.
    pause
    exit /b
)

set RAW_FILE=%~1
set SCRIPT_DIR=%~dp0
set PY_SCRIPT=%SCRIPT_DIR%raw_to_table.py

set PYTHON=
if exist "C:/Users/31479/.workbuddy/binaries/python/envs/default/Scripts/python.exe" (
    set PYTHON=C:/Users/31479/.workbuddy/binaries/python/envs/default/Scripts/python.exe
) else if exist "C:/ProgramData/Miniconda3/python.exe" (
    set PYTHON=C:/ProgramData/Miniconda3/python.exe
) else (
    where python >nul 2>nul
    if errorlevel 1 (
        echo ERROR: Python not found
        pause
        exit /b 1
    )
    set PYTHON=python
)

echo.
echo Parsing: %RAW_FILE%
echo.

"%PYTHON%" "%PY_SCRIPT%" "%RAW_FILE%"
