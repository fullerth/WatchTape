from django.conf.urls import patterns, url

from player_list import views

urlpatterns = patterns('',
    url(r'^player/$', views.view_bouts_by_player, name='bouts_by_player'),
    url(r'^bout/$', views.view_players_by_bout, name='player_by_bout'),
    url(r'^video/bout/$', views.view_videos_by_bout, name='videos_by_bout'),
    url(r'^video/player/$', views.view_videos_by_player, name='video_by_player'),
    url(r'^video/player_bout/$', views.view_videos_by_player_and_bout, name='video_by_player_and_bout'),
    )