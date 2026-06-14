@echo off
setlocal enabledelayedexpansion
title RAW to Origin XRD Stack

if "%~1"=="" (
    echo Bruker RAW to Origin XRD Stack Plot
    echo Drag one or more .raw files onto this bat icon.
    echo Output: Origin graph with Y-offset stacking + opju saved.
    pause
    exit /b
)

set SCRIPT_DIR=%~dp0
set PY_SCRIPT=%SCRIPT_DIR%raw_to_origin.py

:: Use Miniconda Python (has originpro + numpy)
set PYTHON=
if exist "C:/ProgramData/Miniconda3/python.exe" (
    set PYTHON=C:/ProgramData/Miniconda3/python.exe
) else if exist "C:/Users/31479/.workbuddy/binaries/python/envs/default/Scripts/python.exe" (
    set PYTHON=C:/Users/31479/.workbuddy/binaries/python/envs/default/Scripts/python.exe
) else (
    where python >nul 2>nul
    if errorlevel 1 (
        echo ERROR: Python not found
        pause
        exit /b 1
    )
    set PYTHON=python
)

:: Collect all dragged file paths
set FILES=
for %%f in (%*) do set FILES=!FILES! "%%~f"

echo.
echo Parsing and pushing to Origin...
echo Files: %*
echo.

"%PYTHON%" "%PY_SCRIPT%" !FILES!
