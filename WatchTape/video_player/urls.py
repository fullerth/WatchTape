from django.conf.urls import patterns, url

from video_player import views

#already matched /watchtape/
urlpatterns = patterns('',
    url(r'^video_player/(?P<bout_id>\d+)/$',
        views.view_video_player, name='video_player'),
    )