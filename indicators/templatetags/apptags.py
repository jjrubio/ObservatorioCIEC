from django import template

register = template.Library()

@register.filter
def in_category(subcategories, category):
    return subcategories.filter(category=category)

@register.filter
def in_subcategory(indicators, subcategory):
    return indicators.filter(subcategory=subcategory)

@register.filter
def in_position(indicators, position):
    indicator = indicators.filter(id=position)[0]
    return indicator.name