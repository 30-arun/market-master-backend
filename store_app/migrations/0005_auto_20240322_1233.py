# Generated by Django 3.2.8 on 2024-03-22 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0004_auto_20240322_1232'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='templates',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='usertemplate',
            options={'ordering': ['-updated_at']},
        ),
    ]
