from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse
from django.template import RequestContext, loader

#/template
def template(request):
    context = {}
    return render(request, 'template.html', context)

def home(request):
    context = {}
    return render(request, 'base_site.html', context)