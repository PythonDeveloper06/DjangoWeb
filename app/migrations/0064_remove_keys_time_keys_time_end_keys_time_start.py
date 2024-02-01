# Generated by Django 4.2.2 on 2024-01-07 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0063_alter_keys_selection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keys',
            name='time',
        ),
        migrations.AddField(
            model_name='keys',
            name='time_end',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='keys',
            name='time_start',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]