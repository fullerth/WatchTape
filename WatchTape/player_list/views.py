from django.shortcuts import render

from django.http import HttpResponse

#/player/<id>
def view_bouts_by_player(context, player_id):
    return HttpResponse("Viewing bouts of player id %s" % player_id)

#/bout/<id>
def view_players_by_bout(context, bout_id):
    return HttpResponse("Viewing players of bout id %s" % bout_id)

#/videos/bout/<id>
def view_videos_by_bout(context, bout_id):
    return HttpResponse("Viewing videos of bout id %s" % bout_id)

#/videos/player/<id>
def view_videos_by_player(context, player_id):
    return HttpResponse("Viewing videos of player id %s" % player_id)

#/videos/player_bout/<id>_<id>/
def view_videos_by_player_and_bout(context, bout_id, player_id):
    return HttpResponse("Viewing videos of player id %s at bout id %s" % (player_id, bout_id))