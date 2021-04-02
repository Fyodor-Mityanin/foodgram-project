from django import template
from ..models import Favorite, Recipe

register = template.Library()

@register.filter
def is_favorite(recipe, user):
    favorite = Favorite.objects.filter(user=user, recipe=recipe).exists()
    return favorite