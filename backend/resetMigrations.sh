#!/bin/bash

# Delete migrations folders for users and projects apps
rm -rf users/migrations
rm -rf projects/migrations

# Delete the db.sqlite3 file
rm db.sqlite3

# Execute makemigrations for users app
python3 manage.py makemigrations users

# Execute makemigrations for projects app
python3 manage.py makemigrations projects

# Execute migrations
python3 manage.py migrate

# Create superuser for CustomAccount model
echo "from users.models import CustomAccount; CustomAccount.objects.create_superuser('zevind25@gmail.com', 'd', 'z', '1')" | python3 manage.py shell

# Run the server
python3 manage.py runserver

