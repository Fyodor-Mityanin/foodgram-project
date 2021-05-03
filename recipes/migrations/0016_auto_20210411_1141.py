# Generated by Django 3.1.7 on 2021-04-11 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0015_auto_20210407_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='tags_in_recipe',
            field=models.ManyToManyField(blank=True, through='recipes.TagsInRecipe', to='recipes.Tag', verbose_name='Тэги'),
        ),
    ]