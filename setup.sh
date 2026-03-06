#!/bin/bash

# Create necessary directories
echo "Creating project directories..."
mkdir -p data src/data_engineering src/retrieval src/llm src/app src/evaluation notebooks tests

# Create empty __init__.py files to make them Python packages
touch src/__init__.py
touch src/data_engineering/__init__.py
touch src/retrieval/__init__.py
touch src/llm/__init__.py
touch src/app/__init__.py
touch src/evaluation/__init__.py

# Initialize Python Virtual Environment
echo "Setting up virtual environment..."
python3.10 -m venv .venv
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

echo "Setup complete! To activate the environment, run: source .venv/bin/activate"
