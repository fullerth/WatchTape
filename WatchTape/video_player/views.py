from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse
from django.template import RequestContext, loader

from player_list.models import Bout, Jam, Video, VideoToJam

from django.utils import simplejson

#/video_player/video/<video_id>
def view_video_player(request, video_id):
    video = get_object_or_404(Video.objects.select_related('VideoToJam'), pk=video_id)
#    bout = Bout(Bout, pk=bout_id)
#    jams = Jam.objects.select_related('videos').filter(bout__id__exact=bout_id)

    jam_videos = VideoToJam.objects.filter(video__id__exact=video_id)

    times = []

    for jam_video in jam_videos:
        print(jam_video.start_seconds)
        times.append(jam_video.start_seconds)

    js_jams = simplejson.dumps(times)

    context = {'times' : times }
    return render(request, 'video_player/video_player.html', context)