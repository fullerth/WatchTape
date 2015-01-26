from django.conf.urls import patterns, url

from video_player import views

#already matched /watchtape/
urlpatterns = patterns('',
    url(r'^video/(?P<video_id>\d+)/$',
        views.view_video_player, name='video_player'),
    url(r'^stopwatch/(?P<video_id>\d+)/$',
        views.view_stopwatch, name='stopwatch'),
    url(r'^jam_timer/bout/(?P<bout_id>\d+)/$', views.view_jam_timer,
        name='video_jam_timer'),
    )