# Generated by Django 4.2.11 on 2024-03-31 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_newproduct'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreviewProduct',
            fields=[
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=125)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='products/')),
                ('brand', models.CharField(blank=True, max_length=125, null=True)),
                ('description', models.TextField()),
                ('rating', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('numReviews', models.IntegerField(blank=True, default=0, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('countinStock', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
