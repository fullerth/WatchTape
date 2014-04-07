import os
import datetime

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
    populate()
