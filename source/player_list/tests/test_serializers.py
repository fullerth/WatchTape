from django.test import TestCase

from player_list.models import VideoToJam, Video, Jam, Bout
from player_list.serializers.VideoToJamSerializer import VideoToJamSerializer

class VideoToJamSerializerTestCase(TestCase):
    def _create_video_to_jam_data(self):
        video = Video()
        video.save()
        bout = Bout()
        bout.save()
        jam = Jam()
        jam.bout = bout
        jam.save()

        return({'video' : video, 'jam': jam, 'bout': bout})


    def test_create_a_video_to_jam(self):
        dict = self._create_video_to_jam_data()
        data = {'video': dict['video'], 'jam': dict['jam']}
        v_to_j_serializer = VideoToJamSerializer()
        v_to_j = v_to_j_serializer.create(data)

        self.assertIsInstance(v_to_j, VideoToJam,
                              msg="VideoToJamSerializer creating incorrect instance")

