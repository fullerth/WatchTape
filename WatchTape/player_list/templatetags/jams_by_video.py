from django import template
from django.shortcuts import get_object_or_404

from player_list.models import Jam, Video

register = template.Library()

@register.inclusion_tag('player_list/item_by_sort.html')
def jams_by_video(video_id):
    jams = Jam.objects.filter(videotojam__video__id__exact=video_id)
    video = get_object_or_404(Video, pk=video_id)
    context = {'sort' : video, 'items' : jams,
               'sort_name' : video, 'item_name' : 'Jam',
               'url_prefix' : 'jam'}
    return context