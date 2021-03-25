from recipes.models import Recipe, User
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
        context['author'] = self.author
        return context
