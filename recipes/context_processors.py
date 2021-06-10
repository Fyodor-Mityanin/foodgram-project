from django.db.models import BooleanField, Case, Value, When

from .models import Tag


def tags_link_generator(tag, tag_list):
    link = '?'
    tmp_tag_list = tag_list.copy()
    if tag in tmp_tag_list:
        if len(tmp_tag_list) == 1:
            link += f'tag={tmp_tag_list[0]}&'
            return link[:-1]
        tmp_tag_list.remove(tag)
        for i in tmp_tag_list:
            link += f'tag={i}&'
        return link[:-1]
    tmp_tag_list.append(tag)
    for i in tmp_tag_list:
        link += f'tag={i}&'
    return link[:-1]


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
