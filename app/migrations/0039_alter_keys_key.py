# Generated by Django 4.1.6 on 2023-06-05 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0038_alter_devicemodel_serial_num_keys'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keys',
            name='key',
            field=models.IntegerField(max_length=4),
        ),
    ]