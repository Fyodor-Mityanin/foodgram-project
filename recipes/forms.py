from recipes.models import Recipe
from django.forms import models
from .models import Recipe


class RecipeForm(models.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'title',
            'image',
            'description',
            'ingredients_in_recipe',
            'tags_in_recipe',
            'time_to_cook',
        )
