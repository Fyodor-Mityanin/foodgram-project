from recipes.models import Recipe, User, Follow, Favorite, Purchase, Tag
from django.shortcuts import get_object_or_404, HttpResponse
from .models import Recipe
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import RecipeForm
from pytils.translit import slugify
from django.template import loader
from itertools import chain


def get_tags(obj, context):
    context['tags'] = Tag.objects.all()
    if not obj.tag_list:
        context['tag_list'] = ['breakfast', 'lunch', 'dinner']
        return context
    context['tag_list'] = obj.tag_list
    return context


class Index(ListView):
    """Список всех рецептов."""
    model = Recipe
    paginate_by = 6
    template_name = 'index.html'
    context_object_name = 'recipe'

    def get_queryset(self):
        self.tag_list = self.request.GET.getlist('tag')
        if not self.tag_list:
            return Recipe.objects.all()
        return Recipe.objects.filter(tags_in_recipe__slug__in=self.tag_list).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_tags(self, context)
        return context


class NewRecipe(LoginRequiredMixin, CreateView):
    """Создание нового рецепта"""
    # model = Recipe
    template_name = 'new_recipe.html'
    # fields = [
    #     'title',
    #     'image',
    #     'description',
    #     'ingredients_in_recipe',
    #     'tags_in_recipe',
    #     'time_to_cook',
    # ]
    form_class = RecipeForm

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['tags'] = Tag.objects.all()
    #     return context

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
        self.tag_list = self.request.GET.getlist('tag')
        if not self.tag_list:
            return Recipe.objects.filter(author=self.author)
        return Recipe.objects.filter(author=self.author, tags_in_recipe__slug__in=self.tag_list).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            follow = Follow.objects.filter(
                user=self.request.user, author=self.author).exists()
        except TypeError:
            follow = False
        context['author'] = self.author
        context['follow'] = follow
        get_tags(self, context)
        return context


class FavoriteList(LoginRequiredMixin, ListView):
    """Список любимых рецептов."""
    paginate_by = 6
    template_name = 'favorite.html'
    context_object_name = 'recipe'

    def get_queryset(self):
        self.tag_list = self.request.GET.getlist('tag')
        favorites = Favorite.objects.select_related(
            'recipe').filter(user=self.request.user)
        recipe_list = []
        for i in favorites:
            recipe_list.append(i.recipe.id)
        if not self.tag_list:
            return Recipe.objects.filter(pk__in=recipe_list)
        return Recipe.objects.filter(pk__in=recipe_list, tags_in_recipe__slug__in=self.tag_list).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_tags(self, context)
        return context


class RecipeDetail(DetailView):
    """Страница рецепта"""
    model = Recipe
    template_name = 'recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = context['recipe']
        try:
            follow = Follow.objects.filter(
                user=self.request.user, author=recipe.author).exists()
        except TypeError:
            follow = False
        context['follow'] = follow
        return context


class FollowList(LoginRequiredMixin, ListView):
    """Список подписок"""
    paginate_by = 3
    template_name = 'follow.html'
    context_object_name = 'author'

    def get_queryset(self):
        follows = Follow.objects.select_related(
            'author').filter(user=self.request.user)
        author_list = []
        for i in follows:
            author_list.append(i.author.id)
        return User.objects.filter(pk__in=author_list)


class PurchaseList(LoginRequiredMixin, ListView):
    """Список покупок."""
    template_name = 'purchase.html'
    context_object_name = 'recipe'

    def get_queryset(self):
        purchase = Purchase.objects.select_related(
            'recipe').filter(user=self.request.user)
        purchase_list = []
        for i in purchase:
            purchase_list.append(i.recipe.id)
        return Recipe.objects.filter(pk__in=purchase_list)


def PurchaseListDownload(request):
    response = HttpResponse(content_type='text/txt')
    response['Content-Disposition'] = 'attachment; filename="purchase_list.txt"'
    purchase_list = Purchase.objects.select_related(
        'recipe').filter(user=request.user)
    ingredients_list = []
    for purchase in purchase_list:
        ingredients_list.append(list(purchase.recipe.ingredients.all()))
    ingredients_list = list(chain(*ingredients_list))
    clean_ingredients_dict = {}
    for ingredient in ingredients_list:
        if ingredient.ingredient in clean_ingredients_dict:
            clean_ingredients_dict[ingredient.ingredient] += ingredient.quantity
            continue
        clean_ingredients_dict[ingredient.ingredient] = ingredient.quantity
    t = loader.get_template('recipe_list.txt')
    c = {'data': clean_ingredients_dict}
    response.write(t.render(c))
    return response
