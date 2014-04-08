from django.shortcuts import render

from django.http import HttpResponse
from django.template import RequestContext, loader

from player_list.models import Player, Bout, PlayerToBout

#/player/<id>
def view_bouts_by_player(request, player_id):
    #get bout id's for all bouts played in by player
    rostered_bouts = Bout.objects.filter(playertobout__player__id__iexact=player_id)
    player = Player.objects.get(pk=player_id)
    context = { 'player' : player, 'bouts' : rostered_bouts}
    return render(request, 'player_list/bouts_by_player.html', context)

#/bout/<id>
def view_players_by_bout(request, bout_id):
    rostered_players = Player.objects.filter(playertobout__bout__id__exact=bout_id)
    bout = Bout.objects.get(pk=bout_id)
    context = { 'players' : rostered_players, 'bout' : bout}
    return render(request, 'player_list/players_by_bout.html', context)

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