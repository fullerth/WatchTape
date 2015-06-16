from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'WatchTape.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^watchtape/', include('player_list.urls')),
    url(r'^watchtape/', include('video_player.urls'))

    #Can use the default bootstrap template to check if bootstrap is working
    #url(r'^template/', 'WatchTape.views.template', name='template'),
    )
