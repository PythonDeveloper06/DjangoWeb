# Generated by Django 4.2.2 on 2023-10-24 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0044_alter_keys_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keys',
            name='key',
            field=models.IntegerField(),
        ),
    ]