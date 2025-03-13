from django import template
from django.apps import apps

from apps.adjudication.rounders import bankers
from apps.adjudication.rounders import standard

register = template.Library()

@register.filter(name='bankers_round')
def bankers_round(num):
    return bankers(num)

@register.filter(name='standard_round')
def standard_round(num):
    return standard(num)
