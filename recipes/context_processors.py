from django.db.models import BooleanField, Case, Value, When
from django.utils import http

from .models import Tag


def tags_link_generator(tag, tag_list):
    tag_dict = {'tag': tag_list.copy()}
    if tag in tag_dict['tag']:
        if len(tag_dict['tag']) == 1:
            return http.urlencode(tag_dict, doseq=True)
        tag_dict['tag'].remove(tag)
        return http.urlencode(tag_dict, doseq=True)
    tag_dict['tag'].append(tag)
    return http.urlencode(tag_dict, doseq=True)


def tags(request):
    active_tags = request.GET.getlist('tag')
    if not active_tags:
        active_tags = [tag.slug for tag in Tag.objects.all()]
    tags = Tag.objects.annotate(
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
