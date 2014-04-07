from django.contrib import admin
from player_list.models import Player, PlayerToBout, Bout

class PlayerInline(admin.StackedInline):
    model = Player
    extra = 3

admin.site.register(Player)
admin.site.register(PlayerToBout)
admin.site.register(Bout)
