# Generated by Django 2.2.1 on 2019-06-22 07:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_product_interested'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='image',
            field=models.ImageField(blank=True, upload_to='static/myapp/client_pic'),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=100, validators=[django.core.validators.MaxValueValidator(1000), django.core.validators.MinValueValidator(0)]),
        ),
    ]
