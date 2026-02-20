#!/usr/bin/env bash
# Exit on error
set -o errexit

cd backend # Ensure we are in the django project root

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
