#!/usr/bin/env bash
# build.sh

# Install all required packages
pip install --upgrade pip
pip install -r requirements.txt

# Collect all static files (CSS, JS, images)
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate
