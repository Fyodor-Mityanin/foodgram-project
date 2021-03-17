# Generated by Django 3.1.7 on 2021-03-10 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20210305_2352'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='ingredients_in_recipe',
            field=models.ManyToManyField(through='recipes.IngredientsInRecipe', to='recipes.Ingredient'),
        ),
    ]