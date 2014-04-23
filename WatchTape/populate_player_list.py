import os
import datetime

#for wftda stats book importer
import xlrd

class wftda_importer_Mar_2014:
    #Note all offsets are zero-indexed, subtract 1 from excel row/column values

     #bout information
    bout = {'sheet_name': 'IGRF', 'venue_row' : 2, 'venue_column' : 1,
            'date_row' : 4, 'date_column' : 1, 'city_row' : 2, 'city_column' : 7,
            'state_row' : 2, 'state_column' : 9}

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
               'home_blockerC_column' : 18, 'away_jammer_column' : 27,
               'away_pivot_column' : 31, 'away_blockerA_column' : 35,
               'away_blockerB_column' : 39, 'away_blockerC_column' : 43}

    def __init__(self, path):
        #location of workbook
        self.stats = xlrd.open_workbook(path)

        self.import_bout()
        self.import_roster()
        self.import_lineups()

    def import_bout(self):
        bout_sheet = self.stats.sheet_by_name(self.bout['sheet_name'])
        venue_name = bout_sheet.cell_value(self.bout['venue_row'], self.bout['venue_column'])
        bout_date = xlrd.xldate_as_tuple(bout_sheet.cell_value(self.bout['date_row'],
                                                               self.bout['date_column']),
                                                               self.stats.datemode)
        bout_datetime = datetime.datetime(bout_date[0], bout_date[1], bout_date[2],
                                          bout_date[3], bout_date[4], bout_date[5], )

        self.bout_id = add_bout(date=bout_datetime, location=venue_name)

    def import_roster(self):
        roster_sheet = self.stats.sheet_by_name(self.roster['sheet_name'])

        for player in range(self.roster['row_start'], self.roster['row_end']):
            if(roster_sheet.cell_type(player, self.roster['home_number_column']) != xlrd.XL_CELL_EMPTY):
                player_number = roster_sheet.cell_value(player, self.roster['home_number_column'])
                player_name = roster_sheet.cell_value(player, self.roster['home_name_column'])
                rostered_player = add_player(name = player_name, number=player_number)
                add_player_to_bout(player=rostered_player, bout = self.bout_id)

            if(roster_sheet.cell_type(player, self.roster['away_number_column']) != xlrd.XL_CELL_EMPTY):
                player_number = roster_sheet.cell_value(player, self.roster['away_number_column'])
                player_name = roster_sheet.cell_value(player, self.roster['away_name_column'])
                rostered_player = add_player(name = player_name, number=player_number)
                add_player_to_bout(player=rostered_player, bout = self.bout_id)

    def import_lineups(self):
        lineup_sheet = self.stats.sheet_by_name(self.lineups['sheet_name'])

        #import jams from both first and second half
        for jam in (i for j in (range(self.lineups['first_half_row_start'],
                                      self.lineups['first_half_row_end']+1),
                                range(self.lineups['second_half_row_start'],
                                      self.lineups['second_half_row_end']+1)) for i in j):
            if(lineup_sheet.cell_type(jam, self.lineups['jam_number_column']) != xlrd.XL_CELL_EMPTY):
                jam_number = lineup_sheet.cell_value(jam, self.lineups['jam_number_column'])
                home_jammer = lineup_sheet.cell_value(jam, self.lineups['home_jammer_column'])
                home_pivot = lineup_sheet.cell_value(jam, self.lineups['home_pivot_column'])
                home_blockerA = lineup_sheet.cell_value(jam, self.lineups['home_blockerA_column'])
                home_blockerB = lineup_sheet.cell_value(jam, self.lineups['home_blockerB_column'])
                home_blockerC = lineup_sheet.cell_value(jam, self.lineups['home_blockerC_column'])
                away_jammer = lineup_sheet.cell_value(jam, self.lineups['away_jammer_column'])
                away_pivot = lineup_sheet.cell_value(jam, self.lineups['away_pivot_column'])
                away_blockerA = lineup_sheet.cell_value(jam, self.lineups['away_blockerA_column'])
                away_blockerB = lineup_sheet.cell_value(jam, self.lineups['away_blockerB_column'])
                away_blockerC = lineup_sheet.cell_value(jam, self.lineups['away_blockerC_column'])

            #figure out how to do this in the iterator for (jam, half)
            if(jam in range(self.lineups['first_half_row_start'],
                            self.lineups['first_half_row_end']+1)):
                half = 1
            else:
                half = 2

            print('%s - half: %s' % (jam,half) )

def import_wftda_stats(path):
    stats = xlrd.open_workbook(path)
    print(stats.sheet_names())

    igrf_sheet = stats.sheet_by_name('IGRF')
    num_rows = igrf_sheet.nrows - 1
    curr_row = -1
    while curr_row < num_rows:
        curr_row += 1
        row = igrf_sheet.row(curr_row)


    #Create importer
    importer = wftda_importer_Mar_2014(path=path)

    #get players in the bout
    #importer.import_roster()

    #get jams in the bout



def populate():
    alex = add_player(name='Alex DeLarge', number=655)
    bill = add_player(name='Bill F. Murray', number=906)
    bamb = add_player(name='''Beatin' Bam!!B''', number=444)
    nelson = add_player(name='Full Nelson', number=123)
    rumble = add_player(name='Rumble Fist', number=9)

    first_bout = add_bout(date=datetime.date(2014, 1, 1), location="Key Arena")
    second_bout = add_bout(date=datetime.date(2014, 2, 1), location="Rats Nest")
    third_bout = add_bout(date=datetime.date(2014, 3, 1), location="Key Arena")
    fourth_bout = add_bout(date=datetime.date(2014, 3, 15), location="Rats Nets")

    add_player_to_bout(player=alex, bout = first_bout)
    add_player_to_bout(player=alex, bout = second_bout)
    add_player_to_bout(player=alex, bout = fourth_bout)

    add_player_to_bout(player=bill, bout=first_bout)
    add_player_to_bout(player=bill, bout=third_bout)

    add_player_to_bout(player=bamb, bout=first_bout)

    add_player_to_bout(player=nelson, bout=fourth_bout)

    for p in Player.objects.all():
        print('- %s -' % p)

    for b in Bout.objects.all():
        print('- %s -' % b)

    for p_to_b in PlayerToBout.objects.all():
        print('- %s -' % p_to_b)

def add_player(name, number):
    p = Player.objects.get_or_create(name=name, number=number)[0]
    return p

def add_bout(date, location):
    b = Bout.objects.get_or_create(date=date, location=location)[0]
    return b

def add_player_to_bout(player, bout):
    p_to_b = PlayerToBout.objects.get_or_create(player=player, bout=bout)[0]
    return p_to_b

if __name__ == '__main__':
    print('Starting player_list population script...')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WatchTape.settings')
    from player_list.models import Player, Bout, PlayerToBout
    #populate()
    import_wftda_stats(path = '../2014.04.12 DLF vs TR.xlsx')
