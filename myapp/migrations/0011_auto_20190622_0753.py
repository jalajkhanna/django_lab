# Generated by Django 2.2.1 on 2019-06-22 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_auto_20190622_0752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='image',
            field=models.ImageField(blank=True, upload_to='myapp/static/myapp/client_pic'),
        ),
    ]