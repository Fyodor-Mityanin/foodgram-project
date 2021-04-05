from django import template
from ..models import Favorite, Purchase

register = template.Library()

@register.filter
def is_favorite(recipe, user):
    favorite = Favorite.objects.filter(user=user, recipe=recipe).exists()
    return favorite

@register.filter
def is_purchase(recipe, user):
    purchase = Purchase.objects.filter(user=user, recipe=recipe).exists()
    return purchase