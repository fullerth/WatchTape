from django import template
from django.shortcuts import get_object_or_404

from player_list.models import Jam, Bout, VideoToJam

register = template.Library()

@register.inclusion_tag('player_list/item_by_sort.html')
def jams_by_bout(bout_id):
    jams = Jam.objects.filter(bout__id__exact=bout_id)
    bout = get_object_or_404(Bout, pk=bout_id)
    videos = VideoToJam.objects.filter(jam__in=jams)
    temp_video = VideoToJam.objects.filter(id__exact=1)[0]
    print(temp_video)
    print(temp_video.timecode_url)

    print('videos: {0}'.format(videos))
    context = {'sort' : bout_id, 'items' : jams,
               'sort_name' : bout, 'item_name' : 'Jams',
               'url_prefix' : 'jam', 'subitems' : videos,
               'include_video_by_jams' : temp_video}
    return context
