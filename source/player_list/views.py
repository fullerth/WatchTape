from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from player_list.models import Player, Bout, PlayerToRoster, \
                               Jam, PlayerToJam, Video, VideoToJam
from player_list.serializers.VideoToJamSerializer import VideoToJamSerializer

@api_view(['GET', 'POST'])
def view_videotojam_list(request):
    '''
    List all videotojam objects, or create a new videotojam
    '''
    if request.method == 'GET':
        videotojams = VideoToJam.objects.all()
        serializer = VideoToJamSerializer(videotojams, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VideoToJamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def view_videotojam_detail(request, videotojam_id):
    '''
    Detail view for a single video to jam object
    '''
    video_to_jam = get_object_or_404(VideoToJam, pk=videotojam_id)

    if request.method == 'GET':
        serializer = VideoToJamSerializer(video_to_jam)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = VideoToJamSerializer(video_to_jam, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        video_to_jam.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



#/player/<id>
def view_player_info(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    context = { 'player' : player, }
    return render(request, 'player_list/player.html', context)

#/bout/<id>
def view_bout_info(request, bout_id):
    bout = get_object_or_404(Bout, pk=bout_id)
    context = { 'bout' : bout, }
    return render(request, 'player_list/bout.html', context)

#/jam/<id>
def view_jam_info(request, jam_id):
    jam = get_object_or_404(Jam, pk=jam_id)
    context = {'jam' : jam, }
    return render(request, 'player_list/jam.html', context)

#/video/<id>
def view_video_info(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    context = {'video' : video, }
    return render(request, 'player_list/video.html', context)
