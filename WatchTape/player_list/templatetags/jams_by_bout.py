from django import template
from django.shortcuts import get_object_or_404

from player_list.models import Jam, Bout, VideoToJam

register = template.Library()

@register.inclusion_tag('player_list/item_by_sort.html')
def jams_by_bout(bout_id):
    jams = Jam.objects.filter(bout__id__exact=bout_id)
    bout = get_object_or_404(Bout, pk=bout_id)
    #videos = VideoToJam.objects.filter(jam__in=jams)
    #temp_video = VideoToJam.objects.filter(jam__id__in=jams)

    videos = []

    print(jams)
    for jam in jams:
        print(jam.id)
        videos.append(VideoToJam.objects.filter(jam__id__exact=jam.id))
        #print(tmp_video)

    item_subitem_zip = zip(jams, videos)
    item_subitem_tuple = list(item_subitem_zip)
    print(item_subitem_tuple)

    print('videos: {0}'.format(videos))
    context = {'sort' : bout_id, 'items' : item_subitem_tuple,
               'sort_name' : bout, 'item_name' : 'Jams',
               'url_prefix' : 'jam', 'subitems' : True}
    return context
