from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
import os


class Util:
  @staticmethod
  def send_email(data):
      from_name = data["from_name"]
      from_email =  f"{from_name} <{settings.EMAIL_SENDER}>"
      subject = data['subject']
      to_email = [data['to_email']]
      contact_name = data.get('user_name', 'User')
      reset_link = data['reset_link']
      
      # Render HTML template
      html_message = render_to_string('email_template.html', {
          'contact_name': contact_name,
          'reset_link': reset_link
      })
      
      text_content = strip_tags(html_message)  # Plain-text version
    
      send_mail(subject, text_content, from_email, to_email, html_message=html_message)