from .models import Tag


def request(request):
    return {'request': request}


def tags(request):
    tags = Tag.objects.all()
    return {'tags': tags}


def get_tags(obj, context):
    if not obj.tag_list:
        context['tag_list'] = ['breakfast', 'lunch', 'dinner']
        return context
    context['tag_list'] = obj.tag_list
    return context


def tags_link_generator(request, tag, tag_list):
    link = '?'
    tmp_tag_list = tag_list.copy()
    if tag in tmp_tag_list:
        tmp_tag_list.remove(tag)
        if not tmp_tag_list:
            return '?tag=None'
        for i in tmp_tag_list:
            link += f'tag={i}&'
        return link[:-1]
    tmp_tag_list.append(tag)
    for i in tmp_tag_list:
        link += f'tag={i}&'
    return link[:-1]
