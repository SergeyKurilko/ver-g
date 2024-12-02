from django import template

register = template.Library()

@register.filter
def float_with_dot(value, decimal_places=1):
    try:
        return f"{value}".replace(',', '.')
    except ValueError:
        return value



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


@register.filter
def calculate_discounted_price(price, discount):
    return price - ((price*discount) / 100)