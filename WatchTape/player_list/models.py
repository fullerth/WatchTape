from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=200)
    number = models.IntegerField(default = 0)

    def _get_url(self):
        '''Construct the URL for this object'''
        return '/watchtape/player/{0}'.format(self.id)
    url = property(_get_url)


    def __str__(self):
        return("%s #%s" % (self.name, self.number))

class Video(models.Model):
    SITES = (
             ('vimeo', '''http://vimeo.com'''),
             ('youtube', '''http://youtube.com'''),
             ('', 'unknown'),
            )
    url = models.URLField(max_length=255)
    source = models.CharField(max_length=200)
    site = models.CharField(max_length = 7, choices=SITES)

    def __str__(self):
        return("Video {0}".format(self.id))

class Bout(models.Model):
    date = models.DateField('date played')
    location = models.CharField(max_length=200)
    players = models.ManyToManyField(Player, through='PlayerToBout')

    def _get_url(self):
        '''Construct the URL for this object'''
        return '/watchtape/bout/{0}'.format(self.id)
    url = property(_get_url)

    def __str__(self):
        return("%s on %s" % (self.location, self.date))

class Jam(models.Model):
    number = models.IntegerField(default=0)
    half = models.IntegerField(default=1)
    players = models.ManyToManyField(Player, through='PlayerToJam')
    videos = models.ManyToManyField(Video, through='VideoToJam')
    bout = models.ForeignKey(Bout)

    def _get_url(self):
        '''Construct the URL for this object'''
        return '/watchtape/jam/{0}'.format(self.id)
    url = property(_get_url)

    def __str__(self):
        return("Jam #{0}".format(self.number))



class VideoToJam(models.Model):
    start_time = models.CharField(max_length=200)
    end_time = models.CharField(max_length=200)
    video = models.ForeignKey(Video)
    jam = models.ForeignKey(Jam)
    timecode_url = models.URLField(max_length=255)

    def _get_url(self):
        '''Should construct url based on site, for now return timecode url'''
        return self.timecode_url
    url = property(_get_url)

    def __str__(self):
        return("Video#{0} for Jam #{1}".format(self.video.id, self.jam.id))



class PlayerToJam(models.Model):
    POSITIONS = (
                 ('B', 'Blocker'),
                 ('J', 'Jammer'),
                 ('P', 'Pivot'),
                )
    player = models.ForeignKey(Player)
    jam = models.ForeignKey(Jam)
    position = models.CharField(max_length=1, choices=POSITIONS)

    def __str__(self):
        return("{0} in {1}".format(self.player.name, self.jam))

class PlayerToBout(models.Model):
    player = models.ForeignKey(Player)
    bout = models.ForeignKey(Bout)
    captain = models.BooleanField(default=False)

    def __str__(self):
        return("%s in %s" % (self.player, self.bout))
