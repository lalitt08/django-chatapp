#!/bin/bash
echo "Running after install..."

# Navigate to the project directory
cd /Django_Chatapp/fundoo

# Activate the virtual environment
source /Django_Chatapp/venv/bin/activate

# Install Python dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
source ~/.bashrc
# Run database migrations
echo "Running migrations..."
python manage.py migrate

# Collect static files (if needed)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Set permissions for the start script
chmod +x /Django_Chatapp/fundoo/start.sh
