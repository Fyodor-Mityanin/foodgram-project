from recipes.models import Recipe, User, Follow, Favorite
from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import RecipeForm
from pytils.translit import slugify


class Index(ListView):
    """Список всех рецептов."""
    model = Recipe
    paginate_by = 6
    template_name = 'index.html'
    context_object_name = 'recipe'


class NewRecipe(LoginRequiredMixin, CreateView):
    """Создание нового рецепта"""
    template_name = 'new_recipe.html'
    form_class = RecipeForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)[:50]
        return super().form_valid(form)


class AuthorList(ListView):
    """Список рецептов автора."""
    paginate_by = 6
    template_name = 'author.html'
    context_object_name = 'recipe'

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        return Recipe.objects.filter(author=self.author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            follow = Follow.objects.filter(
                user=self.request.user, author=self.author).exists()
        except TypeError:
            follow = False
        context['author'] = self.author
        context['follow'] = follow
        return context


class FavoriteList(ListView):
    """Список любимых рецептов."""
    paginate_by = 6
    template_name = 'favorite.html'
    context_object_name = 'recipe'

    def get_queryset(self):
        favorites = Favorite.objects.select_related('recipe').filter(user=self.request.user)
        recipe_list = []
        for i in favorites:
            recipe_list.append(i.recipe.id)
        # print(recipe_list)
        return Recipe.objects.filter(pk__in=recipe_list)
