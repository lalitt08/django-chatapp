#!/bin/bash
echo "Validating service..."

# Check if the Django app is running
if systemctl is-active --quiet django-backend; then
    echo "Django backend service is running."
else
    echo "Django backend service is not running."
    exit 1
fi