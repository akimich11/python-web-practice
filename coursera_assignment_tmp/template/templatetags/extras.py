from django import template


register = template.Library()


@register.filter('inc')
def inc(value, inc_by):
    return str(int(value) + int(inc_by))


@register.simple_tag
def division(a, b, to_int=False):
    div_result = int(a) / int(b)
    if to_int:
        return str(int(div_result))
    return str(div_result)

