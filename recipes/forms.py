from django.forms import (CheckboxSelectMultiple, JSONField,
                          ModelMultipleChoiceField, ValidationError, models)

from recipes.models import Ingredient, IngredientsInRecipe, Recipe, Tag


class RecipeForm(models.ModelForm):
    tags_in_recipe = ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=CheckboxSelectMultiple,
        required=True,
        label='Тэги',
    )
    ingredients_in_recipe = JSONField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        ingredients_ids = []
        cleaned_data['ingredients_in_recipe'] = []
        for key in self.data:
            if 'Ingredient' in key:
                _, id = key.split('_')
                if id not in ingredients_ids:
                    ingredients_ids.append(id)
        if not ingredients_ids:
            self.add_error(
                'ingredients_in_recipe',
                'Нужно выбрать хотя бы один ингредиент'
            )
            return cleaned_data
        unexist_ingredients = []
        for i in ingredients_ids:
            nameIngredient = 'nameIngredient_' + i
            valueIngredient = 'valueIngredient_' + i
            try:
                ingredient = Ingredient.objects.get(
                    title=self.data[nameIngredient]
                )
                cleaned_data['ingredients_in_recipe'].append(
                    (ingredient, int(self.data[valueIngredient]),)
                )
            except Ingredient.DoesNotExist:
                unexist_ingredients.append(self.data[nameIngredient])
        if unexist_ingredients:
            self.add_error(
                'ingredients_in_recipe',
                f'Ингредиентов {unexist_ingredients} нет в базе'
            )
            return cleaned_data
        return cleaned_data

    def clean_slug(self):
        cleaned_data = super().clean()
        slug = cleaned_data['slug']
        if Recipe.objects.filter(slug=slug).exists():
            raise ValidationError(f'Адрес рецепта "{slug}" уже существует, '
                                  'назовите рецепт по-другому')
        return slug

    def save(self):
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate." % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )
        self.instance.save()
        IngredientsInRecipe.objects.filter(recipe=self.instance).delete()
        objs = [
            IngredientsInRecipe(
                recipe=self.instance,
                ingredient=ingredient[0],
                quantity=ingredient[1]
            )
            for ingredient in self.cleaned_data['ingredients_in_recipe']
        ]
        IngredientsInRecipe.objects.bulk_create(objs)
        return self.instance

    class Meta:
        model = Recipe
        fields = (
            'title',
            'image',
            'description',
            'tags_in_recipe',
            'time_to_cook',
        )
