#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"



# Open Konsole terminal and run the script
konsole -e $SCRIPT_DIR/src/main.sh


