# Steps to run this django code

Create an empty .env file in core/settings folder

Copy contents of core/settings/env_config.env file and paste in core/settings/.env file

Add your database credentials to core/settings/.env file




After that run following lines in order:
  
  pip install -r requirements.txt

  python manage.py makemigrations

  python manage.py migrate

  python manage.py loaddata templates.json

  python manage.py loaddata products.json

  python manage.py runserver
