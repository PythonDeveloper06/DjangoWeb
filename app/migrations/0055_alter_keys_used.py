# Generated by Django 4.2.2 on 2023-11-11 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0054_alter_keys_used'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keys',
            name='used',
            field=models.CharField(choices=[('C', 'Constant'), ('T', 'Temporary'), ('O', 'One use')], default='T', max_length=1),
        ),
    ]
