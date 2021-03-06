from django.contrib import admin
from player_list.models import Player, Bout, Video, Jam, VideoToJam, \
                               PlayerToJam, PlayerToRoster, League, Team, Roster

class PlayerInline(admin.StackedInline):
    model = Player
    extra = 3

admin.site.register(Player)
admin.site.register(Bout)
admin.site.register(Video)
admin.site.register(Jam)
admin.site.register(League)
admin.site.register(Team)


admin.site.register(VideoToJam)
admin.site.register(PlayerToJam)
admin.site.register(PlayerToRoster)
admin.site.register(Roster)