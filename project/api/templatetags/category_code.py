from django import template

register = template.Library()

@register.filter
def shortcat(value):
    codemap = {
        10: 'CA',
        30: 'MUS',
        40: 'PER',
        50: 'SNG',
    }
    try:
        result = codemap[value]
    except KeyError:
        result = value
    return result
