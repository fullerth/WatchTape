from django.contrib import admin
from player_list.models import Player, Bout, Video, Jam, VideoToJam, \
                               PlayerToJam, PlayerToBout, JamToBout

class PlayerInline(admin.StackedInline):
    model = Player
    extra = 3

admin.site.register(Player)
admin.site.register(Bout)
admin.site.register(Video)
admin.site.register(Jam)

admin.site.register(VideoToJam)
admin.site.register(PlayerToJam)
admin.site.register(PlayerToBout)
admin.site.register(JamToBout)
