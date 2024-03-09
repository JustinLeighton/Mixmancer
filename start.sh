#!/bin/bash

VENV_DIR=".venv"
REQUIREMENTS_FILE="requirements.txt"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python -m venv "$VENV_DIR"
fi

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

echo "Installing dependencies..."
pip install -r "$REQUIREMENTS_FILE"

echo "Running python app.py..."
python app.py

echo "Deactivating virtual environment..."
deactivate
