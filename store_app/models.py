from django.db import models
# get User model
from django.contrib.auth import get_user_model
from django.utils import timesince
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


User = get_user_model()


TEMPLATE_CHOICES = [
	('Template1', 'Business'),
	('Template2', 'Portfolio'),
	('Template3', 'CleanIt'),
	('Template4', 'Barber Shop'),
	('Template5', 'Tech Inovations'),
]

FONT_CHOICES = [
    ('Roboto', 'Roboto'),
    ('Open Sans', 'Open Sans'),
    ('Lato', 'Lato'),
    ('Montserrat', 'Montserrat'),
    ('Reddit Mono', 'Reddit Mono'),
    ('Edu NSW', 'Edu NSW'),
]

    
class Templates(models.Model):
	image = models.ImageField(upload_to='templates/', blank=True, null=True)
	title = models.CharField(max_length=256, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	html_content = models.TextField(blank=True, null=True)
	html_content1 = models.TextField(blank=True, null=True)
	html_content2 = models.TextField(blank=True, null=True)
	html_content3 = models.TextField(blank=True, null=True)
	css_cotent = models.TextField(blank=True, null=True)
	js_content = models.TextField(blank=True, null=True)
	ecommerce = models.BooleanField(default=False)
	barber = models.BooleanField(default=False)
	customizable = models.BooleanField(default=False)
	template_type = models.CharField(max_length=100, choices=TEMPLATE_CHOICES, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
	
	class Meta:
		ordering = ['-created_at']
	
	def __str__(self):
		return f"Template: {self.title}, Customizable: {self.customizable}, Ecommerce: {self.ecommerce}, ID: {self.id}"

class UserTemplate(models.Model):
	user = models.ForeignKey(User, related_name='templates', on_delete=models.CASCADE)
	template = models.ForeignKey(Templates, related_name="user_templates", on_delete=models.CASCADE, blank=True, null=True)
	image = models.ImageField(upload_to='templates/', blank=True, null=True)
	title = models.CharField(max_length=256, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	html_content = models.TextField(blank=True, null=True)
	html_content1 = models.TextField(blank=True, null=True)
	html_content2 = models.TextField(blank=True, null=True)
	html_content3 = models.TextField(blank=True, null=True)
	css_cotent = models.TextField(blank=True, null=True)
	js_content = models.TextField(blank=True, null=True)
	ecommerce = models.BooleanField(default=False)
	barber = models.BooleanField(default=False)
	font_type = models.CharField(max_length=100, choices=FONT_CHOICES, null=True, blank=True)
	font_family = models.CharField(max_length=100, null=True, blank=True)
	color_theme_pr = models.CharField(max_length=7, null=True, blank=True)
	color_theme_sc = models.CharField(max_length=7, null=True, blank=True)
	business_name = models.CharField(max_length=100, null=True, blank=True)
	business_logo = models.ImageField(upload_to='business_logos/', null=True, blank=True)
	additional_field = models.TextField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def time_since_updated(self):
		return timesince.timesince(self.updated_at)

	def copy_template(self):
		"""
		Copies the relevant data from the linked template.
		"""
		self.image = self.template.image
		self.title = self.template.title
		self.description = self.template.description
		self.html_content = self.template.html_content
		self.css_cotent = self.template.css_cotent
		self.js_content = self.template.js_content
		self.html_content1 = self.template.html_content1
		self.html_content2 = self.template.html_content2
		self.html_content3 = self.template.html_content3
		self.ecommerce = self.template.ecommerce
		self.barber = self.template.barber
  
	def save(self, *args, **kwargs):
		"""
		Overriding the save method to copy template data on creation.
		"""
		if self.template:
			if not self.pk:  # Check if it's a new instance
				self.copy_template()
		super(UserTemplate, self).save(*args, **kwargs)

	class Meta:
		ordering = ['-updated_at']


	def __str__(self):
    		return f"User Template: {self.title}, ID: {self.id}"

class GetStarted(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	business_name = models.CharField(max_length=100)
	template_type = models.CharField(max_length=100, choices=TEMPLATE_CHOICES, default='Template1')
	font_type = models.CharField(max_length=100, choices=FONT_CHOICES, default='Roboto')
	color_theme_pr = models.CharField(max_length=7) 
	color_theme_sc = models.CharField(max_length=7) 
	business_logo = models.ImageField(upload_to='business_logos/', null=True, blank=True)
	additional_field = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __str__(self):
		return self.business_name

	class Meta:
		ordering = ['-created_at']
		
	def save(self, *args, **kwargs):
		if not self.pk:  # If it's a new instance
			# Check if there is a matching template in GetStartedTemplate
			template = Templates.objects.filter(template_type=self.template_type).first()
			if template:
				# If a matching template is found, create GetStartedUserTemplate instance
				user_template_data = {
					'user': self.user,
					'image': self.business_logo,
					'title': self.business_name,
					'description': self.additional_field,
					'font_type': self.font_type,
					'color_theme_pr': self.color_theme_pr,
					'color_theme_sc': self.color_theme_sc,
					'business_name': self.business_name,
					'business_logo': self.business_logo,
					'additional_field': self.additional_field,
					'html_content1': template.html_content1,
					'html_content2': template.html_content2,
					'html_content3': template.html_content3,
					'css_cotent': template.css_cotent,
					'js_content': template.js_content,
					'ecommerce': template.ecommerce,
					'barber': template.barber,
				}
								
				# Add font_link and font_family based on font_type
				if self.font_type == 'Roboto':
					user_template_data['font_family'] = 'Roboto, sans-serif'
				elif self.font_type == 'Open Sans':
					user_template_data['font_family'] = 'Open Sans, sans-serif'
				elif self.font_type == 'Lato':
					user_template_data['font_family'] = 'Lato, sans-serif'
				elif self.font_type == 'Montserrat':
					user_template_data['font_family'] = 'Montserrat, sans-serif'
				elif self.font_type == 'Reddit Mono':
					user_template_data['font_family'] = 'Reddit Mono, monospace'
				else:
					user_template_data['font_family'] = 'Edu NSW ACT Foundation, cursive'
					
				if template.html_content:
					soup = BeautifulSoup(template.html_content, 'html.parser')

					# Find the element with the class 'mainTitle'
					main_title = soup.find_all(class_='mainTitle')
					if main_title:
						for element in main_title:
							element.string = self.business_name
					main_description = soup.find(class_='mainDescription')
					if main_description:
						main_description.string = self.additional_field
					main_img = soup.find(class_='mainImg')
					if main_img:
						main_img['src'] = "http://127.0.0.1:8000/media/business_logos" + "//" + str(self.business_logo)

					# Update the template's html_content in the user_template_data
					user_template_data['html_content'] = str(soup)

				UserTemplate.objects.create(**user_template_data)
				
		super(GetStarted, self).save(*args, **kwargs)

# class TAdmin(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     user_template = models.ForeignKey(UserTemplate, on_delete=models.CASCADE)
    
#     def __str__(self):
#     	return self.user.name
    
# @receiver(post_save, sender=UserTemplate)
# def create_tadmin(sender, instance, created, **kwargs):
#     if created:
#         TAdmin.objects.create(user=instance.user, user_template=instance)
        
# @receiver(post_delete, sender=UserTemplate)
# def delete_tadmin(sender, instance, **kwargs):
#     TAdmin.objects.filter(user=instance.user, user_template=instance).delete()


class Contact(models.Model):
	user_template = models.ForeignKey(UserTemplate, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	email = models.EmailField()
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['-created_at']

class QrCodeHistory(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=256, null=True, blank=True)
	url = models.URLField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)

	def time_since_updated(self):
		return timesince.timesince(self.created_at)

	def __str__(self):
		return f"{self.user.name}: {self.url}"

	class Meta:
		ordering = ['-created_at']
  
class Appointment(models.Model):
	user_template = models.ForeignKey(UserTemplate, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	email = models.EmailField()
	date = models.DateField()
	time = models.TimeField()
	created_at = models.DateTimeField(auto_now_add=True)
 
	def time_since_updated(self):
		return timesince.timesince(self.created_at)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['-created_at']
  

class Booking(models.Model):
	user_template = models.ForeignKey(UserTemplate, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	email = models.EmailField()
	date = models.DateField()
	time = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	def time_since_updated(self):
		return timesince.timesince(self.created_at)

	def __str__(self):
		return f"{self.name} - {self.date} at {self.time}"

	class Meta:
		ordering = ['-created_at']


def print_hours(start_time_str, end_time_str):
    # Convert string times to datetime objects
    start_time = datetime.strptime(start_time_str, '%I %p')
    end_time = datetime.strptime(end_time_str, '%I %p')
    
    # Ensure end_time is after start_time
    if end_time <= start_time:
        end_time += timedelta(days=1)

    # List to store all hours
    hours_list = []

    # Current time starts at start_time
    current_time = start_time
    while current_time < end_time:
        # Append current time in 12-hour format with AM/PM
        hours_list.append(current_time.strftime('%I %p'))
        # Increment by one hour
        current_time += timedelta(hours=1)

    return hours_list

class AvailableTime(models.Model):
	user_template = models.ForeignKey(UserTemplate, on_delete=models.CASCADE)
	date = models.DateField()
	time = models.JSONField(null=True, blank=True)
	startTime = models.CharField(max_length=200, null=True, blank=True)
	endTime = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return str(self.date)

	def save(self, *args, **kwargs):
    		# Create hourly intervals for the time field
		self.time = print_hours(self.startTime, self.endTime)
		super(AvailableTime, self).save(*args, **kwargs)