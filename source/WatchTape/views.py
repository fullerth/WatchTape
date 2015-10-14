from django.shortcuts import render, get_object_or_404, get_list_or_404

from django.http import HttpResponse
from django.template import RequestContext, loader

from player_list.models import Video

from video_player.views import view_video_player

def home(request):
    return (view_video_player(request, video_id=1))