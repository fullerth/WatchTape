from django import template

register = template.Library()

@register.inclusion_tag('item_by_sort.html')
def players_by_jam():