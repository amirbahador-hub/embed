# Generated by Django 4.0.7 on 2022-10-25 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_baseuser_jwt_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baseuser',
            name='jwt_key',
        ),
    ]
