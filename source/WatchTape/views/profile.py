from django.shortcuts import render, get_object_or_404

def profile(request):
    context = {}
    return render(request, 'profile.html', context)