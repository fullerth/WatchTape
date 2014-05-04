from django import template

register = template.Library()

@register.inclusion_tag('item_by_sort.html')
def players_by_bout():
    rostered_players = \
            Player.objects.filter(playertobout__bout__id__exact=bout_id)
    bout = get_object_or_404(Bout, pk=bout_id)
    context = { 'sort' : bout, 'items' : rostered_players,
                'sort_name' : bout, 'item_name' : 'Player',
                'url_prefix': 'player'}
    return render(request, 'player_list/item_by_sort.html', context)