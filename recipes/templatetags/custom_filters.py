from django import template

register = template.Library()


@register.filter
def tags_link_generator(tag, tag_list):
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


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def addclass_to_boundwidget(BoundWidget, css):
    css_list = [css.strip() for css in css.split(',')]
    BoundWidget.data['attrs']['class'] = css_list[0]
    return BoundWidget


@register.filter
def ru_pluralize(value, arg):
    args = arg.split(",")
    number = abs(int(value))
    a = number % 10
    b = number % 100

    if (a == 1) and (b != 11):
        return args[0]
    elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
        return args[1]
    else:
        return args[2]


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()
