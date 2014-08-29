from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse
from django.template import RequestContext, loader

from player_list.models import Bout, Jam, Video, VideoToJam, Team

from django.utils import simplejson

#/video_player/video/<video_id>
def view_video_player(request, video_id):
    video = get_object_or_404(Video.objects.select_related(
                                                'VideoToJam'
                                          ).select_related(
                                                'Jams'
                                          ), pk=video_id)

    jams = Jam.objects.filter(videos__id__exact=video_id)

    jam_videos = VideoToJam.objects.filter(video__id__exact=video_id)

    times = []
    for jam_video in jam_videos:
        times.append(jam_video.start_seconds)
    js_jams = simplejson.dumps(times)


    bout = Bout.objects.filter(jam__videotojam__video__id__exact=video_id)[0]

    context = {'times' : times, 'jams' : jams,}
    return render(request, 'video_player/video_player.html', context)