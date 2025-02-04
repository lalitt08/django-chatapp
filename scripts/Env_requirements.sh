#!/bin/bash

set -e  # Exit on errors

# Activate virtual environment
source /Django_Chatapp/venv/bin/activate

# Install required dependencies
pip3 install -r /Django_Chatapp/requirements.txt
