from django import template
import math

register = template.Library()

@register.filter
def truncate_number(value, n):
    return math.floor(value * 10 ** n) / 10 ** n