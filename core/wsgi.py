"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
# from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()
# application = DjangoWhiteNoise(application)

# from store_app.models import *

# t = Templates.objects.all()

# x = UserTemplate.objects.filter(user_id=1).first()

# print(x.template.user_templates.all())