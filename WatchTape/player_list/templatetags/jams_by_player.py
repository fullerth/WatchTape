from django import template
from django.shortcuts import render, get_object_or_404

from player_list.models import Jam, Player

register = template.Library()

@register.inclusion_tag('player_list/item_by_sort.html')
def jams_by_player(player_id):
    jams = Jam.objects.filter(playertojam__player__id__exact=player_id)
    player = get_object_or_404(Player, pk=player_id)
    context = {'sort' : player_id, 'items' : jams,
               'sort_name' : player, 'item_name' : 'Jams',
               'url_prefix' : 'jam'}
    return (context)