from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from player_list.models import VideoToJam
from player_list.serializers.VideoToJamSerializer import VideoToJamSerializer

@api_view(['GET', 'POST'])
def viewvideotojam_list(request):
    if request.method == 'POST':
        serializer = VideoToJamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    videotojams = VideoToJam.objects.all()
    serializer = VideoToJamSerializer(videotojams, many=True)
    return Response(serializer.data)

