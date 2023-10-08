#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if Python 3 is installed todo I want it to check only on first initialization, afer it is initialized I want it to be skipped.
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Installing..."
    sudo apt update
    sudo apt install python3
else
    echo "Python 3 is already installed."
fi


# Check if virtualenv is installed
if ! command -v virtualenv &> /dev/null; then
    echo "virtualenv is not installed. Installing..."
    sudo apt install virtualenv
else
    echo "virtualenv is already installed."
fi

file_name="$SCRIPT_DIR/initialized.txt"

virtualenv $SCRIPT_DIR/venv

source $SCRIPT_DIR/venv/bin/activate



if [ -e "$file_name" ]; then

    echo "All deps met, initializing..."


else
    echo "Installing required deps..."

    pip install g4f
    pip install urwid
    pip install keyboard

    touch "$file_name"
fi






# Start Jupyter Lab in the background
python $SCRIPT_DIR/summarize.py


# Deactivate the virtual environment
deactivate
