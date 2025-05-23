# Generated by Django 5.1.6 on 2025-03-24 00:00

import django.core.validators
import users.storages_backends
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0003_alter_userprofile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, help_text='Upload a JPG, JPEG, or PNG image.', null=True,
                                    storage=users.storages_backends.ProfilePicStorage(), upload_to='', validators=[
                    django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]),
        ),
    ]
