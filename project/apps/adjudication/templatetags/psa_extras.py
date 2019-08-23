from django import template

register = template.Library()

@register.filter(name='accounting')
def accounting(value):
    """Converts a string into all lowercase"""
    points = float(value)
    if points < 0:
        return "({0})".format(-points)
    return value
