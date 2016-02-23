# -*- coding: utf-8 -*-

import logging
import logging.config
import argparse
import os
import datetime
import re
import abc

#for wftda stats book importer
import xlrd

#for video to jam importer
import json

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'default': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        __name__: {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
logging.config.dictConfig(LOGGING)
log = logging.getLogger(__name__)

class wftda_importer:
    __metaclass__ = abc.ABCMeta

    def __init__(self, path):
        #location of workbook
        self.stats = xlrd.open_workbook(path)

        self.import_bout()
        self.import_roster()
        self.import_lineups()
        self.import_scores()

    @abc.abstractmethod
    def import_bout(self):
        pass

    @abc.abstractmethod
    def import_roster(self):
        pass

    @abc.abstractmethod
    def import_lineups(self):
        pass

    @abc.abstractmethod
    def import_scores(self):
        pass

   

class wftda_importer_Mar_2014(wftda_importer):
    #Note all offsets are zero-indexed, subtract 1 from excel row/column values

     #bout information
    bout = {
            'sheet_name': 'IGRF',
            'venue_row'       : 2,      'venue_column'       : 1,
            'date_row'        : 4,      'date_column'        : 1,
            'city_row'        : 2,      'city_column'        : 7,
            'state_row'       : 2,      'state_column'       : 9,
            'home_league_row' : 7,      'home_league_column' : 1,
            'away_league_row' : 7,      'away_league_column' : 7,
            'home_team_row'   : 8,      'home_team_column'   : 1,
            'away_team_row'   : 8,      'away_team_column'   : 7,
            }

    #roster information
    roster = {'sheet_name':'IGRF',
              'row_start'             : 10,     'row_end'             : 30,
              'home_number_column'    : 1,      'home_name_column'    : 2,
              'away_number_column'    : 7,      'away_name_column'    : 8,

              'home_league_row'       : 7,      'home_league_column' : 1,
              'away_league_row'       : 7,      'away_league_column' : 7,
              'home_team_row'         : 8,      'home_team_column'   : 1,
              'away_team_row'         : 8,      'away_team_column'   : 7,
            }

    #lineups information
    lineups = {'sheet_name':'Lineups',
               'first_half_row_start'  : 3, 'first_half_row_end'    : 40,
               'second_half_row_start' : 49,'second_half_row_end'   : 86,
               'jam_number_column'     : 0,
               'home_jammer_column'    : 2, 'home_pivot_column'     : 6,
               'home_blockerA_column'  : 10, 'home_blockerB_column' : 14,
               'home_blockerC_column'  : 18,
               'away_jammer_column'    : 28, 'away_pivot_column'    : 32,
               'away_blockerA_column'  : 36, 'away_blockerB_column' : 40,
               'away_blockerC_column'  : 44}

    #Score sheet info
    scores = {'sheet_name':'Score',
              'first_half_row_start'     : 3,  'first_half_row_end'       : 40,
              'second_half_row_start'    : 50, 'second_half_row_end'      : 87,
              'jam_number_column'        : 0,  'away_jam_number_column'   : 19,
              'home_team_jam_total_col'  : 16, 'away_team_jam_total_col'  : 35,
              'home_team_bout_total_col' : 17, 'away_team_bout_total_col' : 36,
              }



    #Keep track of players we've added already to allow for easy retrieval
    stored_roster_home = dict()
    stored_roster_away = dict()

    digits_re = re.compile(r'[0-9]*')

    def __init__(self, path):

        #location of workbook
        self.stats = xlrd.open_workbook(path)

        self.import_bout()
        self.import_roster()
        self.import_lineups()
        self.import_scores()

    def import_bout(self):
        bout_sheet = self.stats.sheet_by_name(self.bout['sheet_name'])
        venue_name = bout_sheet.cell_value(self.bout['venue_row'],
                                           self.bout['venue_column'])
        bout_date = xlrd.xldate_as_tuple(
                    bout_sheet.cell_value(self.bout['date_row'],
                                          self.bout['date_column']),
                                          self.stats.datemode)
        bout_datetime = datetime.datetime(bout_date[0], bout_date[1],
                                          bout_date[2], bout_date[3],
                                          bout_date[4], bout_date[5], )

        bout_home_league = bout_sheet.cell_value(self.bout['home_league_row'],
                                                 self.bout['home_league_column'])
        bout_home_team = bout_sheet.cell_value(self.bout['home_team_row'],
                                               self.bout['home_team_column'])
        bout_away_league = bout_sheet.cell_value(self.bout['away_league_row'],
                                                 self.bout['away_league_column'])
        bout_away_team = bout_sheet.cell_value(self.bout['away_team_row'],
                                                 self.bout['away_team_column'])

        (self.home_league_id, self.home_team_id) = self.add_league_team(
                                                league_name=bout_home_league,
                                                team_name=bout_home_team)
        (self.away_league_id, self.away_team_id) = self.add_league_team(
                                                league_name=bout_away_league,
                                                team_name=bout_away_team)

        self.bout_id = self.add_bout(date=bout_datetime, location=venue_name,
                                     home_team_id = self.home_team_id.id,
                                     away_team_id = self.away_team_id.id)

    def import_roster(self):
        roster_sheet = self.stats.sheet_by_name(self.roster['sheet_name'])

        #IGRF forms may have more than 14 players for a non-sanctioned bout
        #This is currently set to import 20 players
        for player_row in range(self.roster['row_start'], self.roster['row_end']):
            log.debug("Importing Player Row: {0}".format(player_row))
            if(roster_sheet.cell_type(player_row,
                                      self.roster['home_number_column']) != xlrd.XL_CELL_EMPTY):
                player_number = roster_sheet.cell_value(player_row,

                                self.roster['home_number_column'])
                player_name_raw = roster_sheet.cell_value(player_row,
                                  self.roster['home_name_column'])


                #Remove \uc289 (� copyright symbol)
                name_tuple = re.subn("[ ]+\uc2a9[ ]+$", '', player_name_raw)
                #if replaced the copyright symbol, the player is a captain
                captain = True if name_tuple[1] else False

                #Do any other required name cleanup here
                player_name = name_tuple[0]
                try:
                    log.debug("Adding {0}#{1} to {2}, captain: {3}".format(
                            player_name,
                            player_number,
                            'home',
                            captain))
                except UnicodeEncodeError as e:
                    log.debug("Home player number {0} has bad name".format(player_number))
                rostered_player = self.add_player(name = player_name,
                                             number=player_number)

                self.add_player_to_roster(player=rostered_player, roster =
                                        self.bout_id.home_roster, captain=captain)

                self.stored_roster_home[player_number] = rostered_player


            if(roster_sheet.cell_type(player_row, self.roster['away_number_column'])
                                              != xlrd.XL_CELL_EMPTY):
                player_number = roster_sheet.cell_value(player_row,
                                self.roster['away_number_column'])

                player_name_raw = roster_sheet.cell_value(player_row,
                              self.roster['away_name_column'])
                #Remove \uc289 (� copyright symbol)
                name_tuple = re.subn("[ ]+\uc2a9[ ]+$", '', player_name_raw)
                #if replaced the copyright symbol, the player is a captain
                captain = True if name_tuple[1] else False

                player_name = name_tuple[0]

                try:
                    log.debug("Adding {0}#{1} to {2}, captain: {3}".format(
                            player_name,
                            player_number,
                            'away',
                            captain))
                except UnicodeEncodeError as e:
                    log.debug("Away Player Number {0} has bad name".format(player_number))

                rostered_player = self.add_player(name = player_name,
                                             number=player_number)


                self.add_player_to_roster(player=rostered_player, roster =
                                        self.bout_id.away_roster, captain=captain)

                self.stored_roster_away[player_number] = rostered_player
            #increment the player_row
            player_row+=1

    def import_lineups(self):
        lineup_sheet = self.stats.sheet_by_name(self.lineups['sheet_name'])

        #import jams from both first and second half
        for jam in (i for j in (range(self.lineups['first_half_row_start'],
                                      self.lineups['first_half_row_end']),
                                range(self.lineups['second_half_row_start'],
                                      self.lineups['second_half_row_end']))
                    for i in j):
            #Only process the rows that have a number in the jam cell
            #TODO: add an elif to handle star passes as those use "SP" in the
            #jam cell
            if(lineup_sheet.cell_type(jam, self.lineups['jam_number_column'])
                                           == xlrd.XL_CELL_NUMBER):
                log.debug("processing row: {0}".format(jam))

                lineup_dict = self.get_jam_lineup(lineup_sheet=lineup_sheet,
                                                  jam=jam)

                #figure out how to do this in the iterator for (jam, half)
                if(jam in range(self.lineups['first_half_row_start'],
                                self.lineups['first_half_row_end']+1)):
                    half = 1
                else:
                    half = 2

                jam_id = self.add_jam(number=lineup_dict['jam_number'],
                                 half=half, bout=self.bout_id)
                log.debug("{0} in half {1}".format(jam_id, half))

                self.add_lineup_to_jam(jam_id=jam_id, lineup_dict=lineup_dict)

    def import_scores(self):
        jam_number = 0
        score_sheet = self.stats.sheet_by_name(self.scores['sheet_name'])
        for row in (i for j in (range(self.scores['first_half_row_start'],
                                      self.scores['first_half_row_end']),
                                range(self.scores['second_half_row_start'],
                                      self.scores['second_half_row_end']))
                    for i in j):
            #figure out how to do this in the iterator for (jam, half)
            if(row in range(self.scores['first_half_row_start'],
                            self.scores['first_half_row_end']+1)):
                half = 1
            else:
                half = 2

            #Only process the rows that have a number in the jam total cell
            if(score_sheet.cell_type(row, self.scores['jam_number_column'])
                                           == xlrd.XL_CELL_NUMBER):
                jam_number = score_sheet.cell_value(row,
                                            self.scores['jam_number_column'])
                home_jam_score = score_sheet.cell_value(row,
                                        self.scores['home_team_jam_total_col'])
                away_jam_score = score_sheet.cell_value(row,
                                        self.scores['away_team_jam_total_col'])
                home_cumulative_score = score_sheet.cell_value(row,
                                        self.scores['home_team_bout_total_col'])
                away_cumulative_score = score_sheet.cell_value(row,
                                        self.scores['away_team_bout_total_col'])
                log.debug("Score row: {0} | Jam: Home {1}:{2} Away | Total: Home {3}:{4} Away".format(
                                                  row, home_jam_score,
                                                  away_jam_score,
                                                  home_cumulative_score,
                                                  away_cumulative_score))
                #SP cells used for passing team, SP* used for team that does not pass
                if(score_sheet.cell_value(row+1, self.scores['jam_number_column'])
                     == "SP"):
                    home_pivot_score = score_sheet.cell_value(row+1,
                                            self.scores['home_team_jam_total_col'])
                    home_star_pass = True
                    log.debug("Home star pass row: {0}, points: {1}".format(
                                                        row, home_pivot_score))
                else:
                    home_pivot_score = 0
                    home_star_pass = False

                if(score_sheet.cell_value(row+1,
                                self.scores['away_jam_number_column']) == "SP"):
                    away_pivot_score = score_sheet.cell_value(row+1,
                                            self.scores['away_team_jam_total_col'])
                    away_star_pass = True
                    log.debug("Away star pass row: {0}, points: {1}".format(
                                                        row, away_pivot_score))
                else:
                    away_pivot_score = 0
                    away_star_pass = False

                self.add_score_to_jam(bout = self.bout_id,
                                 half = half,
                                 jam_number=jam_number,
                                 home_jam_score=home_jam_score,
                                 away_jam_score=away_jam_score,
                                 home_cumulative_score=home_cumulative_score,
                                 away_cumulative_score=away_cumulative_score,
                                 home_pivot_score = home_pivot_score,
                                 away_pivot_score = away_pivot_score,
                                 home_star_pass = home_star_pass,
                                 away_star_pass = away_star_pass)

    def add_lineup_to_jam(self, jam_id, lineup_dict):
        try:
            self.add_player_to_jam(jam=jam_id,
                              player=self.stored_roster_home[
                                          lineup_dict['home_jammer']],
                              position="J")
            self.add_player_to_jam(jam=jam_id,
                              player=self.stored_roster_home[
                                          lineup_dict['home_pivot']],
                              position="P")
            self.add_player_to_jam(jam=jam_id,
                              player=self.stored_roster_home[
                                          lineup_dict['home_blockerA']],
                              position="B")
            self.add_player_to_jam(jam=jam_id,
                              player=self.stored_roster_home[
                                          lineup_dict['home_blockerB']],
                              position="B")
            self.add_player_to_jam(jam=jam_id,
                              player=self.stored_roster_home[
                                          lineup_dict['home_blockerC']],
                               position="B")
            self.add_player_to_jam(jam=jam_id,
                              player=self.stored_roster_away[
                                          lineup_dict['away_jammer']],
                              position="J")
            self.add_player_to_jam(jam=jam_id,
                              player=self.stored_roster_away[
                                          lineup_dict['away_pivot']],
                              position="P")
            self.add_player_to_jam(jam=jam_id,
                              player=self.stored_roster_away[
                                          lineup_dict['away_blockerA']],
                              position="B")
            self.add_player_to_jam(jam=jam_id,
                              player=self.stored_roster_away[
                                          lineup_dict['away_blockerB']],
                              position="B")
            self.add_player_to_jam(jam=jam_id,
                              player=self.stored_roster_away[
                                          lineup_dict['away_blockerC']],
                              position="B")
        except KeyError as e:
            log.info("Jam {0} did not have all positions fielded".format(
                        jam_id)
                     )

    def get_jam_lineup(self, lineup_sheet, jam):
        lineup = dict()
        lineup['jam_number'] = lineup_sheet.cell_value(jam,
                             self.lineups['jam_number_column'])
        lineup['home_jammer'] = lineup_sheet.cell_value(jam,
                              self.lineups['home_jammer_column'])
        lineup['home_pivot'] = lineup_sheet.cell_value(jam,
                             self.lineups['home_pivot_column'])
        lineup['home_blockerA'] = lineup_sheet.cell_value(jam,
                                self.lineups['home_blockerA_column'])
        lineup['home_blockerB'] = lineup_sheet.cell_value(jam,
                                self.lineups['home_blockerB_column'])
        lineup['home_blockerC'] = lineup_sheet.cell_value(jam,
                                self.lineups['home_blockerC_column'])
        lineup['away_jammer'] = lineup_sheet.cell_value(jam,
                              self.lineups['away_jammer_column'])
        lineup['away_pivot'] = lineup_sheet.cell_value(jam,
                             self.lineups['away_pivot_column'])
        lineup['away_blockerA'] = lineup_sheet.cell_value(jam,
                                self.lineups['away_blockerA_column'])
        lineup['away_blockerB'] = lineup_sheet.cell_value(jam,
                                self.lineups['away_blockerB_column'])
        lineup['away_blockerC'] = lineup_sheet.cell_value(jam,
                                self.lineups['away_blockerC_column'])
        log.debug(lineup)

        return lineup

    def add_player(self, name, number):
            #Grab the first set of digits seen, should limit to 4
            number = self.digits_re.search(number).group()
            p = Player.objects.get_or_create(name=name, number=number)[0]
            return p

    def add_bout(self, date, location, home_team_id, away_team_id):
        try:
            b = Bout.objects.get(date=date, location=location,
                                 home_roster__id=home_team_id,
                                 away_roster__id=away_team_id)
        except Bout.DoesNotExist as e:
            log.debug("Bout does not exist, creating")
            b = Bout.objects.create(date=date, location=location)
            b.away_roster = self.add_roster(away_team_id)
            b.home_roster = self.add_roster(home_team_id)
            b.save()
            log.debug("{0} created".format(b))

        log.debug("home roster id: {0}".format(b.home_roster.id))
        log.debug("away roster id: {0}".format(b.away_roster.id))

        return b

    def add_player_to_roster(self, player, roster, captain=False):
        p_to_b = PlayerToRoster.objects.get_or_create(player=player,
                                                      roster=roster,
                                                      captain=captain)[0]
        return p_to_b

    def add_jam(self, number, half, bout):
        log.debug("Adding with Jam {0} to half {1} of bout {2}".format(
                                                            number, half, bout))
        j = Jam.objects.get_or_create(number=number, half=half, bout=bout)[0]
        return j

    def add_player_to_jam(self, jam, player, position):
        p_to_j = PlayerToJam.objects.get_or_create(jam=jam, player=player,
                                                   position=position)[0]
        return p_to_j

    def add_league_team(self, league_name, team_name):
        team = Team.objects.get_or_create(name=team_name)[0]
        league = League.objects.get_or_create(name=league_name, teams_id=team.id)[0]
        return(league, team)


    def add_roster(self, team_id):
        roster = Roster(team_id = team_id)
        roster.save()

        return roster

    def add_score_to_jam(self, bout, half, jam_number, home_jam_score,
                         away_jam_score, home_cumulative_score,
                         away_cumulative_score, home_pivot_score,
                         away_pivot_score, home_star_pass, away_star_pass):
        j = Jam.objects.get(bout=bout, half=half, number=jam_number)
        j.home_jammer_score = home_jam_score
        j.away_jammer_score = away_jam_score
        j.home_cumulative_score = home_cumulative_score
        j.away_cumulative_score = away_cumulative_score
        j.home_pivot_score = home_pivot_score
        j.home_star_pass = home_star_pass
        j.away_pivot_score = away_pivot_score
        j.away_star_pass = away_star_pass
        j.save()


class video_importer:

    def __init__(self):
        pass

    def add_video(self, url, site, start, end,
                  source, jam, bout, player_url):


        v = Video.objects.get_or_create(url=url,
                                        source=source, site=site,
                                        player_url=player_url)[0]

        timecode_url = jam_url_builder(base_url=url, start_time=start,
                                       site='Vimeo')
        v_to_j = VideoToJam.objects.get_or_create(start_time=start,
                                                  end_time=end,
                                                  video=v, jam=jam,
                                                  timecode_url=timecode_url)

    def add_video_to_jam(self, jam_data, half, data, debug=False):

        bout = Bout.objects.get(pk=data['bout']['id'])
        jam = Jam.objects.filter(
                            number=jam_data['number']
                        ).filter(
                            bout__id=bout.id
                        ).filter(
                            half=half)[0]
        log.debug("{0} in half {1}".format(jam, half))
        self.add_video(url=data['video']['url'],
                       site = data['video']['site'],
                       start=jam_data['Start'], end=jam_data['End'],
                       source=data['video']['source'], jam=jam,
                       bout=bout,
                       player_url = data['video']['player_url'])

    def from_json_file(self, path):
        try:
            f = open(path)
            self.data = json.load(f)
        except ValueError as e:
            log.error("JSON formatting error: {0}".format(e))
        except FileNotFoundError as e:
            log.error("File does not exist: {0}. Error: {1}".format(path, e))
        try:
            for jam_data in self.data['Half 1']:
                self.add_video_to_jam(jam_data=jam_data, data=self.data, half=1)

            for jam_data in self.data['Half 2']:
                self.add_video_to_jam(jam_data=jam_data, data=self.data, half=2)
        except KeyError as e:
            log.warning("{0} does not exist".format(e))

def jam_url_builder(base_url, start_time, stop_time=None, site='Vimeo'):
        if(site=='Vimeo'):
            return base_url+'#t='+start_time


def import_video_info(path):
    video_info = video_importer()
    video_info.from_json_file(path=path)

def import_wftda_stats(path):
    #Create importer
    importer = wftda_importer_Mar_2014(path=path)


if __name__ == '__main__':
    log.debug('Starting player_list population script...')

    os.environ['DJANGO_SETTINGS_MODULE'] = 'WatchTape.settings'

    from django import setup
    setup()


    from player_list.models import Player, Bout, PlayerToRoster, Jam, \
                                   PlayerToJam, Video, VideoToJam, \
                                   League, Team, Roster
    #populate()
    #import_wftda_stats(path =  '../bout_data/2014.04.12 DLF vs TR.xlsx')
    import_wftda_stats_M2014(path = '../bout_data/2014.06.07 AST vs JCRG.xlsx')
#     #import_wftda_stats(path = '../bout_data/2014.08.05 RoT vs TheWorld.xlsx')
#     #import_wftda_stats(path = '../bout_data/2014.11.25 SW vs TR.xlsx')
#     import_wftda_stats(path = '../bout_data/2014.12.09 DLF vs SW.xlsx')
#     import_wftda_stats(path = '../bout_data/2014.12.16 DLF vs TR.xlsx')
#     import_wftda_stats(path = '../bout_data/2014.12.16 GD vs SW.xlsx')
#     import_wftda_stats(path=  '../bout_data/2015.01.27 DLF vs SW.xlsx')
    import_wftda_stats_M2014(path = '../bout_data/2014.06.07 RoT vs SVRG.xlsx')
    import_wftda_stats_D2014(path = '../bout_data/Evil v Hulas Jan 30.xlsx')
 
    import_video_info(path='../bout_data/RatVsJet2014.json')
#     #import_video_info(path='../bout_data/RoTvThe World_8_5_14.json')
#     #import_video_info(path='../bout_data/HomeTeam_Scrimmage_Nov_25_2014.json')
#     #import_video_info(path='../bout_data/RoTvThe World_8_5_14.json')
#     import_video_info(path='../bout_data/2014.12.09_Rat_HomeTeam_Scrimmage.json')
#     import_video_info(path='../bout_data/2014.12.16_Rat_HomeTeam_Scrimmage_DLF_TR.json')
#     import_video_info(path='../bout_data/2014.12.16_Rat_HomeTeam_Scrimmage_GD_SW.json')
#     import_video_info(path='../bout_data/2015.01.27_Rat_HomeTeam_Scrimmage_DLF_SW.json')
    import_video_info(path='../bout_data/RoTvsSVRG.json')
    import_video_info(path='../bout_data/2016.1.30_CarnEvilVsHulaHoneys.json')
