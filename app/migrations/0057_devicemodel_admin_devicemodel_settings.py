# Generated by Django 4.2.2 on 2023-11-11 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0056_alter_keys_used'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicemodel',
            name='admin',
            field=models.CharField(default='Off', max_length=10),
        ),
        migrations.AddField(
            model_name='devicemodel',
            name='settings',
            field=models.CharField(default='-', max_length=255),
        ),
    ]
