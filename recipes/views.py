from django.db.models import Subquery, Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core import paginator
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.template import loader
from django.views.generic import DetailView, ListView
from pytils.translit import slugify
from foodgram.settings import RECIPES_PAGINATE_BY, FOLLOWS_PAGINATE_BY

# from .paginator import SafePaginator
from .forms import RecipeForm
from .models import (Favorite, Follow, Ingredient, IngredientsInRecipe,
                     Purchase, Recipe)
from users.models import User


def get_tags(obj, context):
    # context['tags'] = Tag.objects.all()
    if not obj.tag_list:
        context['tag_list'] = ['breakfast', 'lunch', 'dinner']
        return context
    context['tag_list'] = obj.tag_list
    return context


class Index(ListView):
    """Список всех рецептов."""
    model = Recipe
    # paginator_class = SafePaginator
    paginate_by = RECIPES_PAGINATE_BY
    template_name = 'recipes/index.html'
    context_object_name = 'recipe'

    def get_queryset(self):
        self.tag_list = self.request.GET.getlist('tag')
        if not self.tag_list:
            return Recipe.objects.all_with_flags(self.request.user)
        return Recipe.objects.all_with_flags(
            self.request.user
        ).filter(
            tags_in_recipe__slug__in=self.tag_list
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_tags(self, context)
        return context


class AuthorList(ListView):
    """Список рецептов автора."""
    paginate_by = RECIPES_PAGINATE_BY
    template_name = 'recipes/author.html'
    context_object_name = 'recipe'

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        self.tag_list = self.request.GET.getlist('tag')
        if not self.tag_list:
            return Recipe.objects.all_with_flags(
                self.request.user
            ).filter(author=self.author)
        return Recipe.objects.all_with_flags(
            self.request.user
        ).filter(
            author=self.author, tags_in_recipe__slug__in=self.tag_list
        ).distinct()

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
    paginate_by = RECIPES_PAGINATE_BY
    template_name = 'recipes/favorite.html'
    context_object_name = 'recipe'

    def get_queryset(self):
        self.tag_list = self.request.GET.getlist('tag')
        favorites = Favorite.objects.select_related(
            'recipe').filter(user=self.request.user)
        recipe_list = []
        for i in favorites:
            recipe_list.append(i.recipe.id)
        if not self.tag_list:
            return Recipe.objects.all_with_flags(
                self.request.user
            ).filter(pk__in=recipe_list)
        return Recipe.objects.all_with_flags(
            self.request.user
        ).filter(
            pk__in=recipe_list, tags_in_recipe__slug__in=self.tag_list
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_tags(self, context)
        return context


class RecipeDetail(DetailView):
    """Страница рецепта"""
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'

    def get_queryset(self):
        return Recipe.objects.all_with_flags(self.request.user)

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
    paginate_by = FOLLOWS_PAGINATE_BY
    template_name = 'recipes/follow.html'
    context_object_name = 'authors'

    def get_queryset(self):
        follows = Follow.objects.select_related(
            'author'
        ).filter(
            user=self.request.user
        )
        return User.objects.filter(pk__in=Subquery(follows.values('author')))


class PurchaseList(LoginRequiredMixin, ListView):
    """Список покупок."""
    template_name = 'recipes/purchase.html'
    context_object_name = 'purchase'

    def get_queryset(self):
        return Purchase.objects.filter(user=self.request.user)


def PurchaseListDownload(request):
    response = HttpResponse(content_type='text/txt')
    response['Content-Disposition'] = 'attachment; filename="purchase_list.txt"'
    purchase_list = Purchase.objects.filter(user=request.user)
    ingredients_list = IngredientsInRecipe.objects.filter(
        recipe__in=Subquery(purchase_list.values('recipe'))
    ).values(
        'ingredient__title', 'ingredient__dimension'
    ).annotate(
        total_quantity=Sum('quantity')
    )
    t = loader.get_template('recipes/recipe_list.txt')
    c = {'data': ingredients_list}
    response.write(t.render(c))
    return response


@login_required
def new_recipe(request):
    """Создание рецепта"""
    form = RecipeForm(request.POST or None, files=request.FILES or None,)
    if form.is_valid():
        form.instance.author = request.user
        form.instance.slug = slugify(form.instance.title)[:50]
        form.save()
        return redirect(form.instance)

    return render(
        request,
        'recipes/new_recipe.html',
        {'form': form,
         }
    )


@login_required
def recipe_edit(request, slug):
    """Редактирование рецепта"""
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.author != request.user:
        return redirect(recipe.get_absolute_url())
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe,
    )

    if request.method == 'POST':
        ingredients_ids = []
        for key in form.data:
            if 'Ingredient' in key:
                _, id = key.split('_')
                if id not in ingredients_ids:
                    ingredients_ids.append(id)
        ingredient_list = []
        for i in ingredients_ids:
            nameIngredient = 'nameIngredient_' + i
            valueIngredient = 'valueIngredient_' + i
            unitsIngredient = 'unitsIngredient_' + i
            ingredient_list.append(
                (form.data[nameIngredient], form.data[valueIngredient], form.data[unitsIngredient],))
    if form.is_valid() and ingredient_list:
        form.save()
        ingridients_in_current_recipe = recipe.ingredients.all()
        list_for_delete = []
        for ingredient in ingridients_in_current_recipe:
            current_ing = (ingredient.ingredient.title, str(
                ingredient.quantity), ingredient.ingredient.dimension)
            if current_ing not in ingredient_list:
                list_for_delete.append(ingredient.id)
        IngredientsInRecipe.objects.filter(id__in=list_for_delete).delete()
        for ingredient in ingredient_list:
            object, created = IngredientsInRecipe.objects.get_or_create(
                recipe=form.instance, ingredient=Ingredient.objects.get(title=ingredient[0]), quantity=ingredient[1])
            if created:
                object.save()
        return redirect(form.instance)
    return render(
        request,
        'recipes/new_recipe.html',
        {'form': form,
         'recipe': recipe}
    )


@login_required
def recipe_delete(request, slug):
    """Удаление рецепта"""
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.author != request.user:
        return redirect(recipe.get_absolute_url())
    recipe.delete()
    return redirect('recipes/index')


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)
