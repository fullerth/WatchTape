from django import template
from django.shortcuts import get_object_or_404

from player_list.models import Jam, Bout, VideoToJam

register = template.Library()

@register.inclusion_tag('player_list/item_by_sort.html')
def jams_by_bout(bout_id):
    jams = Jam.objects.select_related('videos').filter(bout__id__exact=bout_id)
    bout = get_object_or_404(Bout, pk=bout_id)

    videos = []

    for jam in jams:
        videos.append(VideoToJam.objects.filter(jam__id__exact=jam.id))

    item_subitem_zip = zip(jams, videos)
    item_subitem_tuple = list(item_subitem_zip)

    context = {'sort' : bout_id, 'items' : item_subitem_tuple,
               'sort_name' : bout, 'item_name' : 'Jams',
               'url_prefix' : 'jam', 'subitems' : True}
    return context
