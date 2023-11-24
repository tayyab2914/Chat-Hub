#!/bin/bash

# Build the project
echo "Building the project..."
python3.9 -m pip install -r requirements.txt

echo "Installing urrlib..."

python3.9 -m pip install urllib3==1.26.6

echo "Ending urrlib..."

echo "Make migrations..."
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput

echo "Collect static...."
python3.9 manage.py collectstatic --noinput --clear