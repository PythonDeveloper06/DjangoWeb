# Generated by Django 4.1.6 on 2023-02-27 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_alter_devicemodel_auth_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicemodel',
            name='auth_key',
            field=models.IntegerField(),
        ),
    ]
