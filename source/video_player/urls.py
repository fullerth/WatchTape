from django.conf.urls import patterns, url

from video_player import views

#already matched /watchtape/
urlpatterns = patterns('',
    url(r'^video/(?P<video_id>\d+)/$',
        views.view_video_player, name='video_player'),
    url(r'^controller', views.view_controller,
        name='video_controller'),
    )
