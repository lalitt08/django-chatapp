#!/bin/bash

set -e  # Exit on errors

# Navigate to the app directory
cd /Django_Chatapp/fundoo
source /Django_Chatapp/venv/bin/activate
# Run database migrations
python3 manage.py makemigrations
bash ~/.bashrc

# Restart Django service
sudo systemctl restart django-backend.service
sudo systemctl status django-backend.service
