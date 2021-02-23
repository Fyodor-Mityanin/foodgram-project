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
    measure = models.CharField(
        'Единицы измерения',
        unique=True,
        max_length=15,
    )
    description = models.TextField(
        'Описание ингредиента',
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
    slug = models.SlugField(
        'Краткое название рецепта (англ.)',
        max_length=50,
        unique=True,
        help_text='Введите краткое название рецепта (англ.)'
    )

    measure = models.CharField(
        'Единицы измерения',
        unique=True,
        max_length=15,
    )
    description = models.TextField(
        'Описание ингредиента',
    )

    def __str__(self):
        return self.name


class Post(models.Model):
    text = models.TextField(
        'Текст',
        help_text='Сюда пишем текст поста',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name='Сообщество',
        help_text='Здесь выбираем сообщество',
    )
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        author = self.author
        text = self.text[:15]
        return f'{author} - {text}'

    def short_text(self):
        return self.text[:150]

    short_text.short_description = 'Начало поста'


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    text = models.TextField(
        'Текст',
        help_text='Сюда пишем текст комментария',
    )
    created = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )


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
