from django.conf.urls import patterns, url

from video_player import views

#already matched /watchtape/
urlpatterns = patterns('',
    url(r'^video_player/video/(?P<video_id>\d+)/$',
        views.view_video_player, name='video_player'),
    url(r'^video_player/controller', views.view_controller,
        name='video_controller'),
    )