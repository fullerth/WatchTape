from django.conf.urls import patterns, url

from player_list import views

#already matched /watchtape/
urlpatterns = patterns('',
    url(r'^player/(?P<player_id>\d+)/$',
        views.view_player_info, name='player_info'),
    url(r'^bout/(?P<bout_id>\d+)/$',
        views.view_bout_info, name='bout_info'),
    url(r'^jam/(?P<jam_id>\d+)/$', views.view_jam_info,
        name='jam_info'),
    )