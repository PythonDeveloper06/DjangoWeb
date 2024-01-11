# Generated by Django 4.2.2 on 2024-01-04 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0062_alter_devicemodel_sync'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keys',
            name='selection',
            field=models.CharField(choices=[('-', '0'), ('+1h', '1 hour'), ('+1d', '1 day'), ('+1w', '1 week'), ('+2w', '2 week')], default='-', max_length=100),
        ),
    ]
