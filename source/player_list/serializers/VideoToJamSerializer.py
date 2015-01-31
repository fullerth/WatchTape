from rest_framework import serializers

from player_list.models import VideoToJam

class VideoToJamSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoToJam
        fields = ('id', )


#     pk = serializers.IntegerField(read_only=True)
#     video = serializers.PrimaryKeyRelatedField(read_only=True)
#
#
#     def create(self, validated_data):
#         '''
#         Create and return a new 'VideoToJam' instance, given the validated_data
#         '''
#         return VideoToJam.objects.create(**validated_data)