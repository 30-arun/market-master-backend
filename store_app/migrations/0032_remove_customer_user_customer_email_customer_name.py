# Generated by Django 4.2.11 on 2024-04-03 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0031_customer_service_seeappointment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='user',
        ),
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(default=1, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='name',
            field=models.CharField(default='2012-12-30 19:00', max_length=100),
            preserve_default=False,
        ),
    ]