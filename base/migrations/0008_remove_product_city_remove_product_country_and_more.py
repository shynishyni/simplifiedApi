# Generated by Django 5.0.7 on 2024-08-27 03:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_product_city_product_country_product_lat_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='city',
        ),
        migrations.RemoveField(
            model_name='product',
            name='country',
        ),
        migrations.RemoveField(
            model_name='product',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='product',
            name='long',
        ),
    ]
