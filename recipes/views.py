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
from .paginator import SafePaginator


class Index(ListView):
    """Выводит все рецепты."""
    model = Recipe
    paginate_by = RECIPES_PAGINATE_BY
    template_name = 'recipes/index.html'
    context_object_name = 'recipe'
    paginator_class = SafePaginator

    def get_queryset(self):
        return Recipe.objects.all_with_flags(
            self.request.user, self.request.tags
        )


class AuthorList(ListView):
    """Выводит все рецепты определённого автора."""
    paginate_by = RECIPES_PAGINATE_BY
    template_name = 'recipes/author.html'
    context_object_name = 'recipe'
    paginator_class = SafePaginator

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        return Recipe.objects.all_with_flags(
            self.request.user, self.request.tags, author=self.author
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        follow = (
            self.request.user.is_authenticated
            and self.request.user.authors.filter(author=self.author).exists()  # noqa
        )
        context['author'] = self.author
        context['follow'] = follow
        return context


class FavoriteList(LoginRequiredMixin, ListView):
    """Выводит все рецепты добавленные в избранное."""
    paginate_by = RECIPES_PAGINATE_BY
    template_name = 'recipes/favorite.html'
    context_object_name = 'recipe'
    paginator_class = SafePaginator

    def get_queryset(self):
        favorites = self.request.user.favorites.all()
        return Recipe.objects.all_with_flags(
            self.request.user, self.request.tags, favorites
        )


class RecipeDetail(DetailView):
    """Выводит один рецепт."""
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
        follow = (
            self.request.user.is_authenticated
            and self.request.user.authors.filter(author=recipe.author).exists()  # noqa
        )
        context['follow'] = follow
        return context


class FollowList(LoginRequiredMixin, ListView):
    """Выводит всех авторов на которых подписан пользователь."""
    paginate_by = FOLLOWS_PAGINATE_BY
    template_name = 'recipes/follow.html'
    context_object_name = 'authors'
    paginator_class = SafePaginator

    def get_queryset(self):
        follows = self.request.user.authors.all()
        return User.objects.filter(pk__in=Subquery(follows.values('author')))


class PurchaseList(LoginRequiredMixin, ListView):
    """Выводит все рецепты которые добавлены в список покупок."""
    template_name = 'recipes/purchase.html'
    context_object_name = 'purchase'

    def get_queryset(self):
        return self.request.user.purchases.all().select_related('recipe')


def PurchaseListDownload(request):
    """Выводит список ингредиентов из списка покупок в txt файл."""
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
    """Создаёт новый рецепт."""
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
    """Редактирует рецепт."""
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.author != request.user:
        return redirect(recipe.get_absolute_url())
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe,
    )
    if form.is_valid():
        form.instance.slug = slugify(form.instance.title)[:50]
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
    """Удаляет рецепт."""
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.author != request.user:
        return redirect(recipe.get_absolute_url())
    recipe.delete()
    return redirect('recipes:index')


@ login_required
def purchase_delete(request, slug):
    """Удаляет рецепт из списка покупок."""
    purchase = get_object_or_404(
        Purchase,
        user=request.user,
        recipe__slug=slug,
    )
    purchase.delete()
    return redirect('recipes:purchase')


def page_not_found(request, exception):
    """Выводит страницу 404."""
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    """Выводит страницу 500."""
    return render(request, 'misc/500.html', status=500)
