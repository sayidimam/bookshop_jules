#!/usr/bin/env bash
# Exit on error
set -o errexit

# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Collect static files
# Note: Ensure DB is not required for this step, or use dummy env vars if needed
python manage.py collectstatic --no-input
