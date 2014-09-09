from django import template
from django.shortcuts import get_object_or_404

from player_list.models import Player, Jam

import logging

register = template.Library()

logger = logging.getLogger(__name__)

@register.inclusion_tag('player_list/item_by_sort.html')
def players_by_jam(jam_id, header_properties = "", data_properties = ""):
    players = Player.objects.filter(jam__id__exact=jam_id)
    jam = get_object_or_404(Jam, pk=jam_id)
    context = {'sort' : jam, 'items' : players,
               'sort_name' : jam, 'item_name' : 'Players',
               'url_prefix' : 'player', 'header_properties' : header_properties,
               'data_properties' : data_properties,}
    return context

def order_players(unordered_players):
    '''Orders a set of one teams worth of players for a jam into
    jammer, pivot, then blockers order'''
    print("unordered:{0}".format(unordered_players))
    jammer = unordered_players.filter(playertojam__position = PlayerToJam.Jammer)
    print("jammer:{0}".format(jammer))
    pivot = unordered_players.filter(playertojam__position = 'P')
    blockers = unordered_players.filter(playertojam__position = 'B')

    #Order by jammer, pivot and blockers
    return jammer | pivot | blockers

@register.inclusion_tag('player_list/item_by_sort.html')
def home_players_by_jam(jam_id, header_properties = "", data_properties = ""):
    unordered_players = Player.objects.filter(
                        roster__home_roster__jam__id__exact=jam_id
                        ).filter(
                        jam__id__exact=jam_id
                        )

    #ordered_players = order_players(unordered_players)


    jam = get_object_or_404(Jam, pk=jam_id)
    context = {'sort' : jam, 'items' : unordered_players,
               'sort_name' : jam, 'item_name' : 'Players',
               'url_prefix' : 'player', 'header_properties' : header_properties,
               'data_properties' : data_properties,}
    return context

@register.inclusion_tag('player_list/item_by_sort.html')
def away_players_by_jam(jam_id, header_properties = "", data_properties = ""):
    unordered_players = Player.objects.filter(
                        roster__away_roster__jam__id__exact=jam_id
                        ).filter(
                        jam__id__exact=jam_id
                        )

    #ordered_players = order_players(unordered_players)

    jam = get_object_or_404(Jam, pk=jam_id)
    context = {'sort' : jam, 'items' : unordered_players,
               'sort_name' : jam, 'item_name' : 'Players',
               'url_prefix' : 'player', 'header_properties' : header_properties,
               'data_properties' : data_properties,}
    return context
