from django.shortcuts import render

from django.http import HttpResponse

#/player/<id>
def view_bouts_by_player(context):
    return HttpResponse("Viewing bouts by player")

#/bout/<id>
def view_players_by_bout(context):
    return HttpResponse("Viewing players by bout")

#/videos/bout/<id>
def view_videos_by_bout(context):
    return HttpResponse("Viewing videos by bout")

#/videos/player/<id>
def view_videos_by_player(context):
    return HttpResponse("Viewing videos by player")

#/videos/player_bout/<id>_<id>/
def view_videos_by_player_and_bout(context):
    return HttpResponse("Viewing videos by player and bout")