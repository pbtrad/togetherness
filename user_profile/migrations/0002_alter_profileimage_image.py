# Generated by Django 4.0.2 on 2022-03-02 22:28

from django.db import migrations, models
import user_profile.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=user_profile.models.image_filename),
        ),
    ]