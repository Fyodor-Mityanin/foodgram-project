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
                cleaned_data['ingredients_in_recipe'][ingredient] = int(
                    self.data[valueIngredient]
                )
            except Ingredient.DoesNotExist:
                unexist_ingredients.append(self.data[nameIngredient])

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
        if not ingredients_in_recipe and not unexist_ingredients:
            self.add_error(
                'ingredients_in_recipe',
                'Нужно выбрать хотя бы один ингредиент'
            )
        if unexist_ingredients:
            error_msg = self.list_of_unexist_ingredients(unexist_ingredients)
            clean_ingredients = cleaned_data['ingredients_in_recipe']
            self.add_error('ingredients_in_recipe', f'{error_msg}')
            cleaned_data['ingredients_in_recipe'] = clean_ingredients
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

    def list_of_unexist_ingredients(self, unexist_ingredients):
        if len(unexist_ingredients) == 1:
            return f'Ингредиента {unexist_ingredients[0]} нет в базе'
        list = ', '.join(unexist_ingredients)
        return f'Ингредиентов {list} нет в базе'
