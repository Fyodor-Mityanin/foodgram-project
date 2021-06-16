from django.forms import (CharField, CheckboxSelectMultiple,
                          ModelMultipleChoiceField, ValidationError, models)

from recipes.models import Ingredient, IngredientsInRecipe, Recipe, Tag


class RecipeForm(models.ModelForm):
    tags_in_recipe = ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=CheckboxSelectMultiple,
        required=True,
        label='Тэги',
    )
    ingredients_in_recipe = CharField(required=False)

    class Meta:
        model = Recipe
        fields = (
            'title',
            'image',
            'description',
            'time_to_cook',
        )

    def get_ingredients_ids(self):
        ingredients_ids = []
        for key in self.data:
            if 'Ingredient' in key:
                _, id = key.split('_')
                if id not in ingredients_ids:
                    ingredients_ids.append(id)
        return ingredients_ids

    def get_ingredients_list(self, ids, cleaned_data, unexist_ingredients):
        for i in ids:
            nameIngredient = 'nameIngredient_' + i
            valueIngredient = 'valueIngredient_' + i
            try:
                ingredient = Ingredient.objects.get(
                    title=self.data[nameIngredient]
                )
            except Ingredient.DoesNotExist:
                unexist_ingredients.append(self.data[nameIngredient])
            cleaned_data['ingredients_in_recipe'][ingredient] = int(
                self.data[valueIngredient]
            )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['ingredients_in_recipe'] = {}
        unexist_ingredients = []
        ids = self.get_ingredients_ids()
        self.get_ingredients_list(ids, cleaned_data, unexist_ingredients)
        self.extraclean_ingredients_in_recipe(
            cleaned_data, unexist_ingredients
        )
        return cleaned_data

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if Recipe.objects.filter(slug=slug).exists():
            raise ValidationError(f'Адрес рецепта "{slug}" уже существует, '
                                  'назовите рецепт по-другому')
        return slug

    def clean_tags_in_recipe(self):
        tags_in_recipe = self.cleaned_data['tags_in_recipe']
        if not tags_in_recipe:
            raise ValidationError('Выберите хотя бы один тэг')
        return tags_in_recipe

    def extraclean_ingredients_in_recipe(self, cleaned_data, unexist_ingredients):
        ingredients_in_recipe = cleaned_data['ingredients_in_recipe']
        if not ingredients_in_recipe:
            raise ValidationError('Нужно выбрать хотя бы один ингредиент')
        if unexist_ingredients:
            raise ValidationError(f'Ингредиентов {unexist_ingredients}'
                                  'нет в базе')
        return ingredients_in_recipe

    def save(self):
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate." % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )
        self.instance.save()
        self.instance.ingredients.all().delete()
        objs = [
            IngredientsInRecipe(
                recipe=self.instance,
                ingredient=k,
                quantity=v,
            )
            for k, v in self.cleaned_data['ingredients_in_recipe'].items()
        ]
        IngredientsInRecipe.objects.bulk_create(objs)
        return self.instance
