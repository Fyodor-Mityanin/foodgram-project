from django.forms import (CheckboxSelectMultiple, ModelMultipleChoiceField,
                          models)

from recipes.models import Recipe, Tag


class RecipeForm(models.ModelForm):
    tags_in_recipe = ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=CheckboxSelectMultiple,
        required=True,
        label='Тэги',
    )

    class Meta:
        model = Recipe
        fields = (
            'title',
            'image',
            'description',
            'tags_in_recipe',
            'time_to_cook',
        )
