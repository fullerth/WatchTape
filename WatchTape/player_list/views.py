from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse
from django.template import RequestContext, loader

from player_list.models import Player, Bout, PlayerToBout, Jam, PlayerToJam

#/player/<id>
def view_bouts_by_player(request, player_id):
    #get bout id's for all bouts played in by player
#     rostered_bouts = \
#             Bout.objects.filter(playertobout__player__id__iexact=player_id)
    player = get_object_or_404(Player, pk=player_id)
    context = { 'sort' : player, }#'items' : rostered_bouts,
#                'sort_name' : player, 'item_name' : 'Bouts',
#                'url_prefix' : 'bout'}
    return render(request, 'player_list/player.html', context)

#/bout/<id>
def view_players_by_bout(request, bout_id):
    rostered_players = \
            Player.objects.filter(playertobout__bout__id__exact=bout_id)
    bout = get_object_or_404(Bout, pk=bout_id)
    context = { 'sort' : bout, 'items' : rostered_players,
                'sort_name' : bout, 'item_name' : 'Player',
                'url_prefix': 'player'}
    return render(request, 'player_list/bout.html', context)

#/video/bout/<id>
def view_videos_by_bout(request, bout_id):
    template = loader.get_template('player_list/videos_by_bout.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

#/video/player/<id>
def view_videos_by_player(request, player_id):
    template = loader.get_template('player_list/videos_by_player.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

#/video/player_bout/<id>_<id>/
def view_videos_by_player_and_bout(request, bout_id, player_id):
    template = loader.get_template('player_list/videos_by_player_and_bout.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def view_players_by_jam(request, jam_id):
    players = Player.objects.filter(playertojam__jam__id__exact=jam_id)
    jam = get_object_or_404(Jam, pk=jam_id)
    context = {'sort' : jam, 'items' : players,
               'sort_name' : jam, 'item_name' : 'Players',
               'url_prefix' : 'player'}
    return render(request, 'player_list/jam.html', context)
