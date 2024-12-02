from django import template

register = template.Library()


@register.filter
def pluralize_comments(count):
    if 10 <= count % 100 <= 20:
        return "комментариев"
    if count % 10 == 1:
        return "комментарий"
    elif 2 <= count % 10 <= 4:
        return "комментария"
    else:
        return "комментариев"

