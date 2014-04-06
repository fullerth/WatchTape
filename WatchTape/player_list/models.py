from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=200)
    number = models.IntegerField(default = 0)

    def __str__(self):
        return("%s #%s" % (self.name, self.number))

class PlayerToBout(models.Model):
    player = models.ForeignKey(Player)
    bout = models.ForeignKey('Bout')

    def __str__(self):
        return("%s in %s" % (self.player, self.bout))

class Bout(models.Model):
    date = models.DateTimeField('date played')
    location = models.CharField(max_length=200)

    def __str__(self):
        return("%s on %s" % (self.location, self.date))