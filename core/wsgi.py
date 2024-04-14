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

# from store_app.utils import create_subdomain

# print(create_subdomain('xyz.marketmaster.me', '13.37.204.72'))

from django.conf import settings
from django.core.mail import send_mail
def send_mail_test(email, token='abc'):
    subject = 'Your forget password link'
    message = f'Hi , '
    email_from = settings.EMAIL_SENDER
    recipient_list = [email]
    print(444,email_from,email,token)
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    print(33)
    return True

# print(send_mail_test('adnanashraf4423@gmail.com'))