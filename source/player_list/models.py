from django.db import models
import re
from datetime import date

class Player(models.Model):
    name = models.CharField(max_length=200)
    number = models.CharField(max_length=10)

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
    #URL for vimeo embed code
    player_url = models.CharField(max_length=2000)

    def __str__(self):
        return("Video {0}".format(self.id))

class Bout(models.Model):
    date = models.DateField('date played', default=date.today)
    location = models.CharField(max_length=200)
    home_roster = models.ForeignKey('Roster', related_name='home_roster',
                                    blank=True, null=True)
    away_roster = models.ForeignKey('Roster', related_name='away_roster',
                                    blank=True, null=True)

    def _get_url(self):
        '''Construct the URL for this object'''
        return '/watchtape/bout/{0}'.format(self.id)
    url = property(_get_url)

    def __str__(self):
        return("{0} vs {1} on {2}".format(self.home_roster.team,
                                          self.away_roster.team, self.date))

class Jam(models.Model):
    number = models.IntegerField(default=0)
    half = models.IntegerField(default=1)
    players = models.ManyToManyField(Player, through='PlayerToJam')
    videos = models.ManyToManyField(Video, through='VideoToJam')
    bout = models.ForeignKey(Bout)

    home_jammer_score = models.IntegerField(default=0)
    away_jammer_score = models.IntegerField(default=0)
    home_pivot_score = models.IntegerField(default=0)
    away_pivot_score = models.IntegerField(default=0)
    home_cumulative_score = models.IntegerField(default=0)
    away_cumulative_score = models.IntegerField(default=0)

    home_star_pass = models.BooleanField(default=False)
    away_star_pass = models.BooleanField(default=False)

    def _get_url(self):
        '''Construct the URL for this object'''
        return '/watchtape/jam/{0}'.format(self.id)
    url = property(_get_url)

    def __str__(self):
        return("{2}, Half #{1}, Jam #{0}".format(self.number, self.half,
                                                      self.bout))

class League(models.Model):
    name = models.CharField(max_length=200)
    teams = models.ForeignKey('Team')

    def __str__(self):
        return(self.name)

class Team(models.Model):
    name = models.CharField(max_length=200)
    players = models.ManyToManyField(Player, blank=True, null=True)


    def __str__(self):
        return(self.name)

class Roster(models.Model):
    team = models.ForeignKey(Team)
    players = models.ManyToManyField(Player, through='PlayerToRoster')

    def __str__(self):
        return("Roster id {0} for {1}".format(self.id, self.team))


class Penalty(models.Model):
    BACK_BLOCK = 'B'
    HIGH_BLOCK = 'A'
    LOW_BLOCK = 'L'
    ELBOWS = 'E'
    FOREARMS = 'F'
    BLOCKING_WITH_HEAD = 'H'
    MULTI_PLAYER = 'M'
    OUT_OF_BOUNDS_BLOCK = 'O' #Also covers out of bounds assists
    OUT_OF_BOUNDS_ASSIST = 'O'
    DIRECTION_OF_PLAY = 'C'
    OUT_OF_PLAY = 'P'
    CUTTING = 'X'
    SKATING_OUT_OF_BOUNDS = 'S'
    ILLEGAL_PROCEDURE = 'I'
    INSUBORDINATION = 'N'
    DELAY_OF_GAME = 'Z'
    GROSS_MISCONDUCT = 'G'
    WFTDA_PENALTIES = (
                       (BACK_BLOCK, 'Back Block'),
                       (HIGH_BLOCK, 'High Block'),
                       (LOW_BLOCK, 'Low Block'),
                       (ELBOWS, 'Elbows'),
                       (FOREARMS, 'Forearms'),
                       (BLOCKING_WITH_HEAD, 'Blocking With Head'),
                       (MULTI_PLAYER, 'Multi-Player'),
                       (OUT_OF_BOUNDS_BLOCK, 'Out of Bounds Block/Assist'),
                       (DIRECTION_OF_PLAY, 'Direction of Play'),
                       (OUT_OF_PLAY, 'Out of Play'),
                       (CUTTING, 'Cutting'),
                       (SKATING_OUT_OF_BOUNDS, 'Skating out of bounds'),
                       (ILLEGAL_PROCEDURE, 'Illegal Procedure'),
                       (INSUBORDINATION, 'Insubordination'),
                       (DELAY_OF_GAME, 'Delay of Game'),
                       (GROSS_MISCONDUCT, 'Gross Misconduct'),
                    )
    penalty = models.CharField(max_length=2, choices=WFTDA_PENALTIES)
    player = models.ForeignKey(Player)
    jam_called = models.ForeignKey(Jam, related_name='penalty_jam_called')
    jam_released = models.ForeignKey(Jam, related_name='penalty_jam_released')

class VideoToJam(models.Model):
    def _timecode_validator(self, timecode):
        '''Times must be stored as strings XhYmZs where X, Y and Z are all ints
           **** DOES NOT APPEAR TO BE WORKING, DON"T RELY ON IT****'''
        print('running validator on %s' % timecode)
        def _time_to_int(time):
            if time != '':
                try:
                    int(time)
                except ValueError as e:
                    raise ValidationError(u'%s is not a valid time' % timecode)

        time = timecode.split('h')
        _time_to_int(time[0])
        time = time[1].split('m')
        _time_to_int(time[0])
        time = time[1].split('s')
        _time_to_int(time[0])


    start_time = models.CharField(max_length=200,
                                  validators=[_timecode_validator])
    end_time = models.CharField(max_length=200,
                                validators=[_timecode_validator])
    video = models.ForeignKey(Video)
    jam = models.ForeignKey(Jam)
    timecode_url = models.URLField(max_length=255)

    def _get_url(self):
        '''Should construct url based on site, for now return timecode url'''
        return self.timecode_url
    url = property(_get_url)

    def _start_time_in_seconds(self):
        '''Return the start time in seconds, normally stored as XmYs'''
        time = 0
        time_str = self.start_time.split('h')
        #Handle the case where only XmYs are present. If there is no hour,
        #there will only be one item in the list containing the initial string.
        if (time_str[0] != self.start_time):
            time += int(time_str[0])*3600
            time_str = time_str[1]
        else:
            time_str = time_str[0]
        time_str = time_str.split('m')
        #Handle case for only Ys present
        if (time_str[0] != self.start_time):
            time += int(time_str[0])*60
            time_str = time_str[1]
        else:
            time_str = time_str[0]
        time_str = time_str.split('s')
        time += int(time_str[0])

        return time

    start_seconds = property(_start_time_in_seconds)

    def __str__(self):
        return("Video#{0} for Jam #{1}".format(self.video.id, self.jam.id))



class PlayerToJam(models.Model):
    BLOCKER = 'B'
    JAMMER = 'J'
    PIVOT = 'P'
    POSITIONS = (
                 (BLOCKER, 'Blocker'),
                 (JAMMER, 'Jammer'),
                 (PIVOT, 'Pivot'),
                )
    player = models.ForeignKey(Player)
    jam = models.ForeignKey(Jam)
    position = models.CharField(max_length=1, choices=POSITIONS)

    def __str__(self):
        return("{0} in {1}".format(self.player.name, self.jam))

class PlayerToRoster(models.Model):
    player = models.ForeignKey(Player)
    roster = models.ForeignKey(Roster)
    captain = models.BooleanField(default=False)

    def __str__(self):
        return("%s in %s" % (self.player, self.bout))
