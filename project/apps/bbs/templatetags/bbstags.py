from django import template

register = template.Library()


@register.filter(name='score')
def score(value):
    """Returns the number as percentage with single-digit precision"""
    try:
        value = float(value)
    except (ValueError, TypeError, UnicodeEncodeError):
        return ''
    return '{0:.1f}'.format(value)
