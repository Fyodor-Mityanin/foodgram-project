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

@register.filter
def tags_link_generator(tag, tag_list):
    link = '?'
    tmp_tag_list = tag_list.copy()
    if tag in tmp_tag_list:
        tmp_tag_list.remove(tag)
        for i in tmp_tag_list:
            link += f'tag={i}&'
        return link[:-1]
    tmp_tag_list.append(tag)
    for i in tmp_tag_list:
        link += f'tag={i}&'
    return link[:-1]