from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'video_player.views.view_video_player', {'video_id':1}, 
        name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^video_player/', include('video_player.urls')),
]
