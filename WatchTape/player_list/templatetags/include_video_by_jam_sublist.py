from django import template
from django.shortcuts import get_object_or_404

from player_list.models import Jam, Video, VideoToJam

register = template.Library()

@register.inclusion_tag('player_list/video_by_jam_sublist')
def videos_by_jam_sublist(jam_id):
    videos = VideoToJam.objects.filter(jam__id__exact=jam_id)
    jam = get_object_or_404(Jam, pk=jam_id)
    context = {'sort' : jam_id, 'items' : videos,
               'sort_name' : jam, 'item_name' : 'Videos',
               'url_prefix' : 'video'}
    return(context)