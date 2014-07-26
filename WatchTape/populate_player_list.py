# -*- coding: utf-8 -*-

import os
import datetime
import re

#for wftda stats book importer
import xlrd

#for video to jam importer
import json

class wftda_importer_Mar_2014:
    #Note all offsets are zero-indexed, subtract 1 from excel row/column values

     #bout information
    bout = {'sheet_name': 'IGRF', 'venue_row' : 2, 'venue_column' : 1,
            'date_row' : 4, 'date_column' : 1, 'city_row' : 2,
            'city_column' : 7, 'state_row' : 2, 'state_column' : 9}

    #roster information
    roster = {'sheet_name':'IGRF', 'row_start': 10, 'row_end':29,
              'home_number_column': 1, 'home_name_column' : 2,
              'away_number_column': 7, 'away_name_column': 8,
              'team_name_row' : 8, 'league_name_row': 7,
              'home_team_name_column' : 1, 'home_league_name_column' : 1,
              'away_team_name_column' : 7, 'away_league_name_column' : 7}

    #lineups information
    lineups = {'sheet_name':'Lineups', 'first_half_row_start' : 3,
               'first_half_row_end' : 40, 'second_half_row_start' : 49,
               'second_half_row_end' : 86, 'jam_number_column' : 0,
               'home_jammer_column' : 2, 'home_pivot_column' : 6,
               'home_blockerA_column' : 10, 'home_blockerB_column' : 14,
               'home_blockerC_column' : 18, 'away_jammer_column' : 28,
               'away_pivot_column' : 32, 'away_blockerA_column' : 36,
               'away_blockerB_column' : 40, 'away_blockerC_column' : 44}



    #Keep track of players we've added already to allow for easy retrieval
    stored_roster_home = dict()
    stored_roster_away = dict()

    def __init__(self, path):

        #location of workbook
        self.stats = xlrd.open_workbook(path)

        self.import_bout()
        self.import_roster()
        self.import_lineups()

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

        self.bout_id = self.add_bout(date=bout_datetime, location=venue_name)

    def import_roster(self):
        roster_sheet = self.stats.sheet_by_name(self.roster['sheet_name'])

        for player in range(self.roster['row_start'], self.roster['row_end']):
            if(roster_sheet.cell_type(player,
                                      self.roster['home_number_column'])
                                      != xlrd.XL_CELL_EMPTY):
                player_number = roster_sheet.cell_value(player,
                                self.roster['home_number_column'])
                player_name_raw = roster_sheet.cell_value(player,
                                  self.roster['home_name_column'])


                #Remove \uc289 (� copyright symbol)
                name_tuple = re.subn("[ ]+\uc2a9[ ]+$", '', player_name_raw)
                #if replaced the copyright symbol, the player is a captain
                captain = True if name_tuple[1] else False

                #Do any other required name cleanup here
                player_name = name_tuple[0]
                rostered_player = self.add_player(name = player_name,
                                             number=player_number)

                self.add_player_to_bout(player=rostered_player, bout =
                                        self.bout_id, captain=captain)

                self.stored_roster_home[player_number] = rostered_player


            if(roster_sheet.cell_type(player, self.roster['away_number_column'])
                                              != xlrd.XL_CELL_EMPTY):
                player_number = roster_sheet.cell_value(player,
                                self.roster['away_number_column'])
                player_name = roster_sheet.cell_value(player,
                              self.roster['away_name_column'])
                rostered_player = self.add_player(name = player_name,
                                             number=player_number)
                self.add_player_to_bout(player=rostered_player, bout =
                                        self.bout_id)

                self.stored_roster_away[player_number] = rostered_player

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
                print("processing row: {0}".format(jam))

                lineup_dict = self.get_jam_lineup(lineup_sheet=lineup_sheet,
                                                  jam=jam)

                #figure out how to do this in the iterator for (jam, half)
                if(jam in range(self.lineups['first_half_row_start'],
                                self.lineups['first_half_row_end']+1)):
                    half = 1
                else:
                    half = 2

                jam_id = self.add_jam(number=lineup_dict['jam_number'],
                                 half=half,
                                 bout=self.bout_id)
                print("{0} in half {1}".format(jam_id, half))

                self.add_lineup_to_jam(jam_id=jam_id, lineup_dict=lineup_dict)

    def add_lineup_to_jam(self, jam_id, lineup_dict):
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

        print(lineup)

        return lineup

    def add_player(self, name, number):
        p = Player.objects.get_or_create(name=name, number=number)[0]
        return p

    def add_bout(self, date, location):
        b = Bout.objects.get_or_create(date=date, location=location)[0]
        return b

    def add_player_to_bout(self, player, bout, captain=False):
        p_to_b = PlayerToBout.objects.get_or_create(player=player, bout=bout,
                                                    captain=captain)[0]
        return p_to_b

    def add_jam(self, number, half, bout):
        print("Adding with Jam {0} to half {1} of bout {2}".format(
                                                            number, half, bout))
        j = Jam.objects.get_or_create(number=number, half=half, bout=bout)[0]
        return j

    def add_player_to_jam(self, jam, player, position):
        p_to_j = PlayerToJam.objects.get_or_create(jam=jam, player=player,
                                                   position=position)[0]
        return p_to_j

class video_importer:

    def __init__(self):
        pass

    def add_video(self, url, site, start, end,
                  source, jam, bout):


        v = Video.objects.get_or_create(url=url,
                                        source=source, site=site)[0]

        timecode_url = jam_url_builder(base_url=url, start_time=start,
                                       site='Vimeo')
        v_to_j = VideoToJam.objects.get_or_create(start_time=start,
                                                  end_time=end,
                                                  video=v, jam=jam,
                                                  timecode_url=timecode_url)

    def add_video_to_jam(self, jam_data, half, data):
        bout = Bout.objects.get(pk=data['bout']['id'])
        jam = Jam.objects.filter(
                            number=jam_data['number']
                        ).filter(
                            bout__id=bout.id
                        ).filter(
                            half=half)[0]
        print("{0} in half {1}".format(jam, half))
        self.add_video(url=data['video']['url'],
                       site = data['video']['site'],
                       start=jam_data['Start'], end=jam_data['End'],
                       source=data['video']['source'], jam=jam,
                       bout=bout)

    def from_json_file(self, path):
        try:
            f = open(path)
            self.data = json.load(f)
        except ValueError as e:
            print("JSON formatting error: {0}".format(e))
        except FileNotFoundError as e:
            print("File does not exist: {0}. Error: {1}".format(path, e))

        for jam_data in self.data['Half 1']:
            self.add_video_to_jam(jam_data=jam_data, data=self.data, half=1)

        for jam_data in self.data['Half 2']:
            self.add_video_to_jam(jam_data=jam_data, data=self.data, half=2)


    #Implement
    @classmethod
    def from_wftda_sheet(cls, path):
        pass




def jam_url_builder(base_url, start_time, stop_time=None, site='Vimeo'):
        if(site=='Vimeo'):
            #Should raise an exception if stop_time is defined as vimeo does
            #not support a stop time
            return base_url+'#t='+start_time


def import_video_info(path):
    video_info = video_importer()
    video_info.from_json_file(path=path)

def import_wftda_stats(path):
    #Create importer
    importer = wftda_importer_Mar_2014(path=path)


if __name__ == '__main__':
    print('Starting player_list population script...')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WatchTape.settings')
    from player_list.models import Player, Bout, PlayerToBout, Jam, \
                                   PlayerToJam, Video, VideoToJam
    #populate()
    #import_wftda_stats(path = '../2014.04.12 DLF vs TR.xlsx')
    import_wftda_stats(path = '../2014.06.07 AST vs JCRG.xlsx')

    import_video_info(path='RatVsJet2014.json')
