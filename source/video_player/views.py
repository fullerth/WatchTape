import json
import logging

from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse
from django.template import RequestContext, loader

from django.core.exceptions import ObjectDoesNotExist

from player_list.models import Bout, Jam, Video, VideoToJam, Team, Player, \
                               PlayerToJam, Roster 

logger = logging.getLogger(__name__)

def view_controller(request):
    return render(request, 'video_player/controller.html')

#/video_player/video/<video_id>
def view_video_player(request, video_id):
    video = get_object_or_404(Video, pk=video_id)

    jams = Jam.objects.filter(videos__id__exact=video_id)

    jam_videos = VideoToJam.objects.filter(video__id__exact=video_id)

    times = []
    for jam_video in jam_videos:
        times.append(jam_video.start_seconds)
    js_jams = json.dumps(times)

    def _populate_context():
        context = {'times' : None, 'jams' : None,
               'jams_list' : None, 'video' : None}
        try:
            #This does not work with videos containing more than one bout
            bout = Bout.objects.filter(
                    jam__videotojam__video__id__exact=video_id)[0]
        except IndexError:
            logger.warning("bout for video {0} could not be retrieved".format(
                            video_id))
            return context

        try:
            home_roster = Roster.objects.get(home_roster=bout)
            away_roster = Roster.objects.get(away_roster=bout)
            home_players = home_roster.players
            away_players = away_roster.players
        except ObjectDoesNotExist:
            logger.warning(
              "Roster for bout {0} in video {1} could not be retrieved".format(
               bout.id, video_id))
            return context

        jams_list = []

        for jam in jams:
            try:
                jam_dict = {'roster' : create_roster_dict(jam),
                            'score' : create_score_dict(jam),
                            }
            except IndexError:
                logger.warning(
                    "Could not create roster or score dict for jam {0}".format(
                            jam))
                continue
            jams_list.append(jam_dict)


        context = {'times' : times, 'jams' : jams,
               'jams_list' : jams_list, 'video' : video}
        return context

    context = _populate_context()

    return render(request, 'video_player/video_player.html', context)

def create_roster_dict(jam):
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
    return(roster)

def create_score_dict(jam):
    scores = {'home_cumulative' : jam.home_cumulative_score,
              'away_cumulative' : jam.away_cumulative_score,
              'home_jammer' : jam.home_jammer_score,
              'away_jammer' : jam.away_jammer_score,
              'home_pivot' : jam.home_pivot_score,
              'away_pivot' : jam.away_pivot_score,
              'home_star_pass' : jam.home_star_pass,
              'away_star_pass' : jam.away_star_pass}
    return(scores)
