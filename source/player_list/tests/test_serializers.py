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

    def test_update_a_video_to_jam_time(self):
        dict = self._create_video_to_jam_data()
        first_start_time = '0m10s'
        first_end_time = '0m40s'
        updated_start_time = '5m5s'
        updated_end_time = '6m20s'
        data = {'video' : dict['video'], 'jam' : dict['jam'],
                'start_time' : first_start_time, 'end_time' : first_end_time}
        v_to_j_serializer = VideoToJamSerializer()
        v_to_j = v_to_j_serializer.create(data)

        self.assertEqual(v_to_j.start_time, first_start_time,
                         msg="Initial start time incorrect")
        self.assertEqual(v_to_j.end_time, first_end_time,
                         msg="Initial end time incorrect")

        data['start_time'] = updated_start_time
        data['end_time'] = updated_end_time

        v_to_j_serializer.update(v_to_j, data)

        self.assertEqual(v_to_j.start_time, updated_start_time,
                         msg="Update to start time failed")
        self.assertEqual(v_to_j.end_time, updated_end_time,
                         msg="Update to end time failed")

