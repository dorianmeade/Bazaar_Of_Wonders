from django import template

register = template.Library()

@register.filter
def fix_url(value):
    return value.replace("%20"," ")