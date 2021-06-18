from django.db.models import BooleanField, Case, Value, When
from django.utils.http import urlencode

from .models import Tag


def tags_link_generator(tag, tag_list):
    tag_dict = {'tag': tag_list.copy()}
    if tag in tag_dict['tag']:
        if len(tag_dict['tag']) == 1:
            return urlencode(tag_dict, doseq=True)
        tag_dict['tag'].remove(tag)
        return urlencode(tag_dict, doseq=True)
    tag_dict['tag'].append(tag)
    return urlencode(tag_dict, doseq=True)


def tags(request):
    active_tags = request.GET.getlist('tag')
    tags = Tag.objects.all()
    if not active_tags:
        active_tags = [tag.slug for tag in tags]
    tags = tags.annotate(
        is_active=Case(
            When(slug__in=active_tags, then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        )
    )
    for tag in tags:
        url = tags_link_generator(tag.slug, active_tags)
        tag.url = url
    return {'tags': tags}
