from django import template
from django.shortcuts import render, get_object_or_404

from player_list.models import Bout, Player

register = template.Library()

@register.inclusion_tag('player_list/item_by_sort.html')
def bouts_by_player(player_id):
    #get bout id's for all bouts played in by player
    rostered_bouts = \
            Bout.objects.filter(playertobout__player__id__iexact=player_id)
    player = get_object_or_404(Player, pk=player_id)
    context = { 'sort' : player, 'items' : rostered_bouts,
               'sort_name' : player, 'item_name' : 'Bouts',
               'url_prefix' : 'bout'}
    return (context)