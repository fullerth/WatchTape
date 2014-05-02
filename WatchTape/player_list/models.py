from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=200)
    number = models.IntegerField(default = 0)

    def __str__(self):
        return("%s #%s" % (self.name, self.number))

class Bout(models.Model):
    date = models.DateField('date played')
    location = models.CharField(max_length=200)

    def __str__(self):
        return("%s on %s" % (self.location, self.date))

class Jam(models.Model):
    number = models.IntegerField(default=0)
    half = models.IntegerField(default=1)
    bout = models.ForeignKey(Bout)
    players = models.ManyToManyField(Player, through='PlayerToJam')

    def __str__(self):
        return("Jam #{0}".format(self.number))

class Video(models.Model):
    url = models.URLField(max_length=200)
    Jam = models.ForeignKey(Jam)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)

class PlayerToJam(models.Model):
    POSITIONS = (
                 ('B', 'Blocker'),
                 ('J', 'Jammer'),
                 ('P', 'Pivot')
                )
    player = models.ForeignKey(Player)
    jam = models.ForeignKey(Jam)
    position = models.CharField(max_length=1, choices=POSITIONS)

class PlayerToBout(models.Model):
    player = models.ForeignKey(Player)
    bout = models.ForeignKey(Bout)
    captain = models.BooleanField(default=False)

    def __str__(self):
        return("%s in %s" % (self.player, self.bout))

class JamToBout(models.Model):
    bout = models.ForeignKey(Bout)
    jam = models.ForeignKey(Jam)

class PlayerToJam(models.Model):
    player = models.ForeignKey(Player)
    jam = models.ForeignKey(Jam)
