#!/bin/bash

# Set up Git credential caching
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=3600'

# Install Python 3.11 and its development tools
sudo apt install python3.11
sudo apt install python3.11-venv
sudo apt-get install build-essential
sudo apt-get install python3.11-dev

# Create a Python virtual environment
python3.11 -m venv venv311
source venv311/bin/activate

# Install requirements from a file
pip install -r resources/requirements.txt

# Display the path of the Python interpreter
which python

# Deactivate the virtual environment
deactivate
