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

    #This should get refactored to be a list of dicts for clarity in the template

    home_jammers = []
    home_pivots = []
    home_blockers = []
    away_jammers = []
    away_pivots = []
    away_blockers = []

    for jam in jams:
        home_jammers.append(Player.objects.filter(
                        roster__home_roster__jam__id__exact=jam.id,
                        jam__id__exact=jam.id,
                        playertojam__position__icontains = PlayerToJam.JAMMER
                        )[0])
        home_pivots.append(Player.objects.filter(
                        roster__home_roster__jam__id__exact=jam.id,
                        jam__id__exact=jam.id,
                        playertojam__position__icontains = PlayerToJam.PIVOT
                        )[0])
        home_blockers.append(Player.objects.filter(
                        roster__home_roster__jam__id__exact=jam.id,
                        jam__id__exact=jam.id,
                        playertojam__position__icontains = PlayerToJam.BLOCKER
                        ))
        away_jammers.append(Player.objects.filter(
                        roster__away_roster__jam__id__exact=jam.id,
                        jam__id__exact=jam.id,
                        playertojam__position__icontains = PlayerToJam.JAMMER
                        )[0])
        away_pivots.append(Player.objects.filter(
                        roster__away_roster__jam__id__exact=jam.id,
                        jam__id__exact=jam.id,
                        playertojam__position__icontains = PlayerToJam.PIVOT
                        )[0])
        away_blockers.append(Player.objects.filter(
                        roster__away_roster__jam__id__exact=jam.id,
                        jam__id__exact=jam.id,
                        playertojam__position__icontains = PlayerToJam.BLOCKER
                        ))
        print("processing jam # {0}".format(jam.id))
        print("home_blockers: {0}".format(home_blockers))

    rosters = list(zip(home_jammers, home_pivots, home_blockers,
                       away_jammers, away_pivots, away_blockers))


    context = {'times' : times, 'jams' : jams,
               'rosters' : rosters}
#                'away_jammer' : away_jammer, 'away_pivot' : away_pivot,
#                'away_blockers' : away_blockers,
#                'home_jammer' : home_jammer, 'home_pivot' : home_pivot,
#                'home_blockers' : home_blockers }
    return render(request, 'video_player/video_player.html', context)