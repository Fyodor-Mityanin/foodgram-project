from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    BREAKFAST = 'B'
    LUNCH = 'L'
    DINNER = 'D'
    RECIPE_TAG = [
        (BREAKFAST, 'Завтрак'),
        (LUNCH, 'Обед'),
        (DINNER, 'Ужин'),
    ]
    title = models.CharField(
        'Тэг рецепта',
        choices=RECIPE_TAG,
        max_length=1,
    )

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(
        'Название ингредиента',
        unique=True,
        max_length=200,
    )
    dimension = models.CharField(
        'Единицы измерения',
        max_length=15,
    )

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    title = models.CharField(
        'Название рецепта',
        unique=True,
        max_length=200,
    )
    image = models.ImageField(
        upload_to='recipes/',
        blank=True,
        null=True
    )
    description = models.TextField(
        'Описание ингредиента',
    )
    ingredients_in_recipe = models.ManyToManyField(
        Ingredient,
        through='IngredientsInRecipe',
    )
    slug = models.SlugField(
        'Краткое название рецепта (англ.)',
        max_length=50,
        unique=True,
        help_text='Введите краткое название рецепта (англ.)'
    )
    time_to_cook = models.PositiveSmallIntegerField(
        'Время готовки в минутах',
        help_text='Введите год выпуска произведения'
    )

    def __str__(self):
        return self.title


class IngredientsInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Ингредиент',
    )
    quantity = models.PositiveSmallIntegerField(
        'Количество',
        help_text='Сколько класть?'
    )

    def __str__(self):
        recipe = self.recipe
        ingredients = self.ingredient
        quantity = self.quantity
        return f'{recipe}-{ingredients}-{quantity}'


class TagsInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='tags',
        verbose_name='Рецепт',
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Ингредиент',
    )

    def __str__(self):
        recipe = self.recipe
        tag = self.tag
        return f'{recipe}-{tag}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписота',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        unique_together = ['user', 'author']
