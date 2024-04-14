
import environ
from .base import *
import os

DEBUG = True

SECRET_KEY= env("SECRET_KEY")

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://0.0.0.0:3000",
    "http://127.0.0.1:3000"
]

# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME': env('CLOUD_NAME'),
#     'API_KEY': env('CLOUD_API_KEY'),
#     'API_SECRET': env('CLOUD_API_SECRET'),
# }
#
# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
database = env('DATABASE')

if database == 'POSTGRESQL':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env('DB_NAME'),
            'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASSWORD'),
            'HOST': env('DB_HOST'),
            'PORT': env('DB_PORT'),
        }
    }
elif database == 'MYSQL':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': env('DB_NAME'),
            'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASSWORD'),
            'HOST': env('DB_HOST'),
            'PORT': env('DB_PORT'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
        }
    }


# STRIPE_PUBLISHABLE_KEY=env("STRIPE_PUBLISHABLE_KEY")
# STRIPE_SECRET_KEY=env("STRIPE_SECRET_KEY")

# CURRENT_ADMIN_DOMAIN = env("CURRENT_ADMIN_DOMAIN")
#
# EMAIL_ADMIN = env("EMAIL_ADMIN")





STRIPE_PUBLIC_KEY=env("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY=env("STRIPE_SECRET_KEY")

HOSTED_ZONE_ID = env("HOSTED_ZONE_ID")
AWS_ACCESS_KEY_ID=env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY=env("AWS_SECRET_ACCESS_KEY")


# SendGrid
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API_KEY')
EMAIL_SENDER = env('EMAIL_SENDER')