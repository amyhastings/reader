# Generated by Django 4.2.16 on 2025-03-16 13:45

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='profile_pics'),
        ),
    ]
