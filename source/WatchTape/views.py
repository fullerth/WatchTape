from django.shortcuts import render, get_object_or_404, get_list_or_404

from django.http import HttpResponse
from django.template import RequestContext, loader

from player_list.models import Video

#/template
def template(request):
    context = {}
    return render(request, 'template.html', context)

def home(request):
    videos = get_list_or_404(Video)
    context = {'videos': videos}
    return render(request, 'base_site.html', context)