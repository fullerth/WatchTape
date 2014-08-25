from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse
from django.template import RequestContext, loader

from player_list.models import Player, Bout, PlayerToRoster, \
                               Jam, PlayerToJam, Video

#/player/<id>
def view_player_info(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    context = { 'player' : player, }
    return render(request, 'player_list/player.html', context)

#/bout/<id>
def view_bout_info(request, bout_id):
    bout = get_object_or_404(Bout, pk=bout_id)
    context = { 'bout' : bout, }
    return render(request, 'player_list/bout.html', context)

#/jam/<id>
def view_jam_info(request, jam_id):
    jam = get_object_or_404(Jam, pk=jam_id)
    context = {'jam' : jam, }
    return render(request, 'player_list/jam.html', context)

#/video/<id>
def view_video_info(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    context = {'video' : video, }
    return render(request, 'player_list/video.html', context)
