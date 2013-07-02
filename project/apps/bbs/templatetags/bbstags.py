from django import template
from django.utils.timezone import localtime

register = template.Library()


@register.filter(name='score')
def score(value):
    """Returns the number as percentage with single-digit precision"""
    try:
        value = float(value)
    except (ValueError, TypeError, UnicodeEncodeError):
        return ''
    return '{0:.1f}'.format(value)


@register.filter(expects_localtime=True, name='time_only')
def time_only(value):
    """Returns the number as percentage with single-digit precision"""
    try:
        value = localtime(value)
        value = value.timetz()
    except (ValueError, TypeError, UnicodeEncodeError):
        return ''
    return '{:%H:%M}'.format(value)
