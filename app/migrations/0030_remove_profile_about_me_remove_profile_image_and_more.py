# Generated by Django 4.1.6 on 2023-03-14 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_rename_bio_profile_about_me_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='about_me',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='image',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
    ]
