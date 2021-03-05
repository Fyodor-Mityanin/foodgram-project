from django.contrib.auth.decorators import login_required
from recipes.models import Recipe
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Recipe

def index(request):
    recipes_list = Recipe.objects.all()
    paginator = Paginator(recipes_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator}
    )
