from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Subquery, Sum
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.template import loader
from django.views.generic import DetailView, ListView
from pytils.translit import slugify

from foodgram.settings import FOLLOWS_PAGINATE_BY, RECIPES_PAGINATE_BY
from users.models import User

from .forms import RecipeForm
from .models import IngredientsInRecipe, Purchase, Recipe


class Index(ListView):
    """Список всех рецептов."""
    model = Recipe
    paginate_by = RECIPES_PAGINATE_BY
    template_name = 'recipes/index.html'
    context_object_name = 'recipe'

    def get_queryset(self):
        tag_list = self.request.GET.getlist('tag')
        return Recipe.objects.all_with_flags(
            self.request.user, tag_list
        )


class AuthorList(ListView):
    """Список рецептов автора."""
    paginate_by = RECIPES_PAGINATE_BY
    template_name = 'recipes/author.html'
    context_object_name = 'recipe'

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        tag_list = self.request.GET.getlist('tag')
        return Recipe.objects.all_with_flags(
            self.request.user, tag_list
        ).filter(
            author=self.author
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            follow = self.request.user.authors.filter(
                author=self.author
            ).exists()
        except AttributeError:
            follow = False
        context['author'] = self.author
        context['follow'] = follow
        return context


class FavoriteList(LoginRequiredMixin, ListView):
    """Список любимых рецептов."""
    paginate_by = RECIPES_PAGINATE_BY
    template_name = 'recipes/favorite.html'
    context_object_name = 'recipe'

    def get_queryset(self):
        tag_list = self.request.GET.getlist('tag')
        favorites = self.request.user.favorites.all()
        return Recipe.objects.all_with_flags(
            self.request.user, tag_list
        ).filter(
            pk__in=Subquery(favorites.values('recipe'))
        )


class RecipeDetail(DetailView):
    """Страница рецепта"""
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'

    def get_object(self):
        recipe = Recipe.objects.all_with_flags(
            self.request.user
        ).get(
            slug=self.kwargs['slug']
        )
        return recipe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = context['recipe']
        try:
            follow = self.request.user.authors.filter(
                author=recipe.author
            ).exists()
        except AttributeError:
            follow = False
        context['follow'] = follow
        return context


class FollowList(LoginRequiredMixin, ListView):
    """Список подписок"""
    paginate_by = FOLLOWS_PAGINATE_BY
    template_name = 'recipes/follow.html'
    context_object_name = 'authors'

    def get_queryset(self):
        follows = self.request.user.authors.all()
        return User.objects.filter(pk__in=Subquery(follows.values('author')))


class PurchaseList(LoginRequiredMixin, ListView):
    """Список покупок."""
    template_name = 'recipes/purchase.html'
    context_object_name = 'purchase'

    def get_queryset(self):
        return self.request.user.purchases.all()


def PurchaseListDownload(request):
    response = HttpResponse(content_type='text/txt')
    response['Content-Disposition'] = 'attachment; filename="purchase_list.txt"'
    purchase_list = request.user.purchases.all()
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


@ login_required
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


@ login_required
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
    if form.is_valid():
        form.save()
        return redirect(form.instance)
    return render(
        request,
        'recipes/new_recipe.html',
        {'form': form,
         'recipe': recipe}
    )


@ login_required
def recipe_delete(request, slug):
    """Удаление рецепта"""
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.author != request.user:
        return redirect(recipe.get_absolute_url())
    recipe.delete()
    return redirect('/')


@ login_required
def purchase_delete(request, slug):
    """Удаление покупки"""
    purchase = get_object_or_404(
        Purchase,
        user=request.user,
        recipe__slug=slug,
    )
    purchase.delete()
    return redirect('purchase')


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)
