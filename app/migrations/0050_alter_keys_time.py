# Generated by Django 4.2.2 on 2023-11-09 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0049_alter_keys_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keys',
            name='time',
            field=models.DateTimeField(default=None),
        ),
    ]