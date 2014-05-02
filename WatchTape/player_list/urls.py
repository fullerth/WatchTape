from django.conf.urls import patterns, url

from player_list import views

#already matched /watchtape/
urlpatterns = patterns('',
    url(r'^player/(?P<player_id>\d+)/$',
        views.view_bouts_by_player, name='bouts_by_player'),
    url(r'^bout/(?P<bout_id>\d+)/$',
        views.view_players_by_bout, name='player_by_bout'),
    url(r'^video/bout/(?P<bout_id>\d+)/$',
        views.view_videos_by_bout, name='videos_by_bout'),
    url(r'^video/player/(?P<player_id>\d+)/$',
        views.view_videos_by_player, name='video_by_player'),
    url(r'^video/player_bout/(?P<player_id>\d+)_(?P<bout_id>\d+)/$',
        views.view_videos_by_player_and_bout, name='video_by_player_and_bout'),
    url(r'^jam/player/(?P<player_id>\d+)/$',
        views.view_jams_by_player, name='jams_by_player')
    )