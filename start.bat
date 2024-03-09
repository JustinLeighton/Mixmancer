@echo off

set VENV_DIR=.venv
set REQUIREMENTS_FILE=requirements.txt

if not exist %VENV_DIR% (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
)

echo Activating virtual environment...
call %VENV_DIR%\Scripts\activate

echo Installing dependencies...
pip install -r %REQUIREMENTS_FILE%

echo Running Mixmancer app...
python app.py

echo Deactivating virtual environment...
deactivate
