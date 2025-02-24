@echo off

:: Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3 and try again.
    exit /b 1
)

:: Install requirements
pip install -r requirements.txt

python thing.py