from django.conf.urls import patterns, url

from player_list import views

#already matched /watchtape/
urlpatterns = patterns('',
    url(r'^videotojam/$', views.viewvideotojam_list,
            name='videotojam_list'),
    )