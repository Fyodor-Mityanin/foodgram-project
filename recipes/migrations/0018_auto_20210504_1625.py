# Generated by Django 3.1.7 on 2021-05-04 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0017_auto_20210411_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='time_to_cook',
            field=models.PositiveSmallIntegerField(verbose_name='Время приготовления'),
        ),
    ]
