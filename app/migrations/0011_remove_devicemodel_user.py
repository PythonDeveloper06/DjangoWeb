# Generated by Django 4.1.6 on 2023-02-26 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_devicemodel_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devicemodel',
            name='user',
        ),
    ]
