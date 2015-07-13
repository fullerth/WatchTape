from rest_framework import serializers

from player_list.models import VideoToJam

class VideoToJamSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoToJam
        fields = ('id', 'start_time', 'end_time', 'video', 'jam', 'timecode_url')