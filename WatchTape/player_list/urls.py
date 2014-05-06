from django.conf.urls import patterns, url

from player_list import views

#already matched /watchtape/
urlpatterns = patterns('',
    url(r'^player/(?P<player_id>\d+)/$',
        views.view_bouts_by_player, name='bouts_by_player'),
    url(r'^bout/(?P<bout_id>\d+)/$',
        views.view_players_by_bout, name='player_by_bout'),
    url(r'^jam/(?P<jam_id>\d+)/$', views.view_players_by_jam,
        name='players_by_jam'),
    )