#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Run generate_env.py
python scripts/generate_env.py
