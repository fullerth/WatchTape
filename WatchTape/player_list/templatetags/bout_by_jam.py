from django import template
from django.shortcuts import get_object_or_404

from player_list.models import Bout, Jam

register = template.Library()

@register.inclusion_tag('player_list/item_by_sort.html')
def bout_by_jam(jam_id):
    bout = Jam.objects.filter(bout__id__exact=bout_id)
    jam = get_object_or_404(Jam, pk=jam_id)
    context = {'sort' : jam_id, 'items' : players,
               'sort_name' : jam, 'item_name' : 'Players',
               'url_prefix' : 'player'}
    return context