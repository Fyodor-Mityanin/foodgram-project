from django.contrib.auth import get_user_model, get_user
from django.db import models
from django.urls import reverse

User = get_user_model()


class Tag(models.Model):
    title = models.CharField(
        'Имя тэга',
        unique=True,
        max_length=10,
    )
    slug = models.SlugField(
        'Слаг тэга',
        unique=True,
        max_length=10,
        blank=True
    )
    color = models.CharField(
        'Цвет тэга',
        max_length=10,
        blank=True
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
    tags_in_recipe = models.ManyToManyField(
        Tag,
        through='TagsInRecipe',
        blank=True,
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
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/recipe/%s/' % self.slug

    class Meta:
        ordering = ['-pub_date']

    # def favorites_flag(self):
    #     try:
    #         favorite = Favorite.objects.filter(user=get_user(), recipe=self)
    #     except TypeError:
    #         favorite = False
    #     return user


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
        verbose_name='Тэг',
    )

    class Meta:
        unique_together = ['recipe', 'tag']

    def __str__(self):
        recipe = self.recipe
        tag = self.tag
        return f'{recipe}-{tag}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authors',
        verbose_name='Юзер',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        unique_together = ['user', 'author']


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Юзер',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='likers',
        verbose_name='Рецепт',
    )

    class Meta:
        unique_together = ['user', 'recipe']

class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='Purchases',
        verbose_name='Юзер',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='buyers',
        verbose_name='Рецепт',
    )

    class Meta:
        unique_together = ['user', 'recipe']
