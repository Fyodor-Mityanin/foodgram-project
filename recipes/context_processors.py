from django.db.models import BooleanField, Case, Value, When
from django.utils.http import urlencode

from .models import Tag


def tag_remove(tag, tag_dict):
    if len(tag_dict['tag']) == 1:
        tag.url = urlencode(tag_dict, doseq=True)
        return tag
    tag_dict['tag'].remove(tag.slug)
    tag.url = urlencode(tag_dict, doseq=True)
    return tag


def tag_append(tag, tag_dict, len_tags):
    tag_dict['tag'].append(tag.slug)
    if len(tag_dict['tag']) == len_tags:
        tag_dict['tag'] = []
    tag.url = urlencode(tag_dict, doseq=True)
    return tag


def tags_link_generator(tags):
    active_tags = []
    for tag in tags:
        if tag.is_active:
            active_tags.append(tag.slug)
    for tag in tags:
        tag_dict = {'tag': active_tags.copy()}
        if tag.slug in tag_dict['tag']:
            tag_remove(tag, tag_dict)
            continue
        tag_append(tag, tag_dict, len(tags))
    return tags


def tags(request):
    active_tags = request.GET.getlist('tag')
    if not active_tags:
        tags = Tag.objects.annotate(
            is_active=Value(True, output_field=BooleanField())
        )
    else:
        tags = Tag.objects.annotate(
            is_active=Case(
                When(slug__in=active_tags, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )
    tags_link_generator(tags)
    return {'tags': tags}
