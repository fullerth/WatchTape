from django import template
from django.shortcuts import get_object_or_404

from player_list.models import Jam, Bout, VideoToJam

register = template.Library()

@register.inclusion_tag('player_list/item_by_sort.html')
def jams_by_bout(bout_id):
    jams = Jam.objects.filter(bout__id__exact=bout_id)
    bout = get_object_or_404(Bout, pk=bout_id)
    videos = VideoToJam.objects.filter(jam__in=jams)
    print('videos: {0}'.format(videos))
    context = {'sort' : bout_id, 'items' : jams,
               'sort_name' : bout, 'item_name' : 'Jams',
               'url_prefix' : 'jam', 'subitems' : videos}
    return context