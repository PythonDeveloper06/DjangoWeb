# Generated by Django 4.1.6 on 2023-02-22 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_devicemodel_status_lock_devicemodel_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicemodel',
            name='status',
            field=models.CharField(default='Close', max_length=10),
        ),
    ]
