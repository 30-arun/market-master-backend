# Generated by Django 4.2.11 on 2024-03-26 16:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store_app', '0012_remove_coupon_cart_remove_order_cart_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GetStarted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=100)),
                ('template_type', models.CharField(choices=[('Template1', 'Template 1'), ('Template2', 'Template 2')], max_length=100)),
                ('font_type', models.CharField(choices=[('Arial', 'Arial'), ('Times_New_Roman', 'Times New Roman'), ('Verdana', 'Verdana')], max_length=100)),
                ('color_theme', models.CharField(max_length=7)),
                ('business_logo', models.ImageField(blank=True, null=True, upload_to='business_logos/')),
                ('additional_field', models.TextField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
