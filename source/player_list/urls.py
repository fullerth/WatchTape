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
    url(r'^video/(?P<video_id>\d+)/$', views.view_video_info,
        name='video_info'),
    url(r'^videotojam/$', views.view_videotojam_list,
        name='videotojam_list'),
    url(r'^videotojam/(?P<videotojam_id>\d+)/$', views.view_videotojam_detail,
        name='videotojam_detail')
    )