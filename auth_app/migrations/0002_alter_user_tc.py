# Generated by Django 5.0.6 on 2024-06-18 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='tc',
            field=models.BooleanField(default=False),
        ),
    ]
