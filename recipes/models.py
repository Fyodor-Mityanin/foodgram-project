from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from users.models import User


class RecipeQuerySet(models.QuerySet):
    def all_with_flags(self, user, tag_list=None, favorites=None, author=None):
        qs = self
        if tag_list:
            qs = self.filter(tags_in_recipe__slug__in=tag_list)
        if favorites:
            qs = qs.filter(pk__in=models.Subquery(favorites.values('recipe')))
        if author:
            qs = qs.filter(author=author)
        if user.is_anonymous:
            return qs.distinct()
        favorite = Favorite.objects.filter(
            recipe=models.OuterRef('pk'),
            user=user
        )
        purchase = Purchase.objects.filter(
            recipe=models.OuterRef('pk'),
            user=user
        )
        return qs.annotate(
            is_favorite=models.Exists(favorite),
            is_purchase=models.Exists(purchase),
        ).distinct()


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

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

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

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

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
        null=True,
        verbose_name='Загрузить фото',
    )
    description = models.TextField(
        'Описание',
    )
    ingredients_in_recipe = models.ManyToManyField(
        Ingredient,
        through='IngredientsInRecipe',
        verbose_name='Ингредиенты',
    )
    tags_in_recipe = models.ManyToManyField(
        Tag,
        through='TagsInRecipe',
        verbose_name='Тэги',
    )
    slug = models.SlugField(
        'Краткое название рецепта (англ.)',
        max_length=50,
        unique=True,
        help_text='Введите краткое название рецепта (англ.)'
    )
    time_to_cook = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[
            MinValueValidator(
                1,
                'Время готовки не может быть ноль или меньше'
            ),
        ],
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    objects = RecipeQuerySet.as_manager()

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe', kwargs={'slug': self.slug})

    def short_description(self):
        return self.description[:150]

    def num_in_favorite(self):
        return self.likers.count()

    def list_of_tags(self):
        tag_list = [tag.tag for tag in self.tags.all()]
        return tag_list

    short_description.short_description = 'Описание'
    num_in_favorite.short_description = 'Кол-во лайков'
    list_of_tags.short_description = 'Тэги'


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
        help_text='Сколько класть?',
        validators=[
            MinValueValidator(
                1,
                'Количество ингредиентов не может быть ноль или меньше'
            )
        ],
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        unique_together = ['recipe', 'ingredient']

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
        verbose_name = 'Тэг рецепта'
        verbose_name_plural = 'Тэги рецепта'

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
        constraints = [
            models.CheckConstraint(
                name='prevent_self_follow',
                check=~models.Q(user=models.F('author'))
            ),
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_users_in_folllow'
            ),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


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
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
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
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
