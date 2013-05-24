from django import template

register = template.Library()

def isodd(value):
    return bool(value/2)

register.filter(isodd)