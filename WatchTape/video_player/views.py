from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse
from django.template import RequestContext, loader

from player_list.models import Bout

#/video_player/<bout_id>
def view_video_player(request, bout_id):
    bout = get_object_or_404(Bout, pk=bout_id)
    context = {}
    return render(request, 'video_player/video_player.html', context)