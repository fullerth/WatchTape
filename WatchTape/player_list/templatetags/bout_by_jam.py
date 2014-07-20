from django import template
from django.shortcuts import get_object_or_404
from django.template import Context

from player_list.models import Bout, Jam #JamToBout

register = template.Library()

@register.inclusion_tag('player_list/item_by_sort.html')
def bout_by_jam(jam_id):
    bout = Bout.objects.filter(jam__id__exact=jam_id)
    jam = get_object_or_404(Jam, pk=jam_id)
    new_context = {'sort' : jam, 'items' : bout,
               'sort_name' : jam, 'item_name' : 'Bout',
               'url_prefix' : 'bout'}
    return Context(new_context)