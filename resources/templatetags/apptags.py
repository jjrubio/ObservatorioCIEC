from django import template

register = template.Library()

@register.filter
def in_category(links, category):
    return links.filter(category=category)
