from django import template
from django.shortcuts import get_object_or_404

from player_list.models import Bout, Player

register = template.Library()

@register.inclusion_tag('player_list/item_by_sort.html')
def players_by_bout(bout_id):
    rostered_players = \
            Player.objects.filter(playertobout__bout__id__exact=bout_id)
    bout = get_object_or_404(Bout, pk=bout_id)
    context = { 'sort' : bout, 'items' : rostered_players,
                'sort_name' : bout, 'item_name' : 'Player',
                'url_prefix': 'player'}
    return context