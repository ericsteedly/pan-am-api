#!/bin/bash

rm -rf panamapi/migrations
rm db.sqlite3
python manage.py makemigrations panamapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata customers
python manage.py loaddata airports
python manage.py loaddata flights