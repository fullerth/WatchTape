from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse
from django.template import RequestContext, loader

from player_list.models import Bout, Jam, Video, VideoToJam, Team, Player, \
                               PlayerToJam

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

    rosters = []

    for jam in jams:
        roster = {}
        roster['home_jammer'] = Player.objects.filter(
                        roster__home_roster__jam__id__exact=jam.id,
                        jam__id__exact=jam.id,
                        playertojam__position__icontains = PlayerToJam.JAMMER
                        )[0]
        roster['home_pivot'] = Player.objects.filter(
                        roster__home_roster__jam__id__exact=jam.id,
                        jam__id__exact=jam.id,
                        playertojam__position__icontains = PlayerToJam.PIVOT
                        )[0]
        roster['home_blockers'] = Player.objects.filter(
                        roster__home_roster__jam__id__exact=jam.id,
                        jam__id__exact=jam.id,
                        playertojam__position__icontains = PlayerToJam.BLOCKER
                        )
        roster['away_jammer'] = Player.objects.filter(
                        roster__away_roster__jam__id__exact=jam.id,
                        jam__id__exact=jam.id,
                        playertojam__position__icontains = PlayerToJam.JAMMER
                        )[0]
        roster['away_pivot'] = Player.objects.filter(
                        roster__away_roster__jam__id__exact=jam.id,
                        jam__id__exact=jam.id,
                        playertojam__position__icontains = PlayerToJam.PIVOT
                        )[0]
        roster['away_blockers'] = Player.objects.filter(
                        roster__away_roster__jam__id__exact=jam.id,
                        jam__id__exact=jam.id,
                        playertojam__position__icontains = PlayerToJam.BLOCKER
                        )
        rosters.append(roster)

    context = {'times' : times, 'jams' : jams,
               'rosters' : rosters}
    return render(request, 'video_player/video_player.html', context)