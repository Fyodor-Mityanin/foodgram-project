# Generated by Django 3.1.7 on 2021-03-05 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='measure',
            new_name='unit',
        ),
    ]
