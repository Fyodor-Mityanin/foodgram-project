from recipes.models import Recipe, Tag
from django.forms import models, ModelMultipleChoiceField, CheckboxSelectMultiple
from .models import Recipe


class RecipeForm(models.ModelForm):
    tags_in_recipe = ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=CheckboxSelectMultiple,
        required=True)

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
