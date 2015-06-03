from django.test import TestCase

from player_list.models import VideoToJam, Video, Jam, Bout
from player_list.serializers.VideoToJamSerializer import VideoToJamSerializer

class VideoToJamSerializerTestCase(TestCase):
    def _create_video_to_jam_data(self, video_pk=1, bout_pk=1, jam_pk=1):
        video = Video.objects.create(pk=video_pk)
        bout = Bout.objects.create(pk=bout_pk)
        jam = Jam.objects.create(pk=jam_pk, bout=bout)

        return({'video' : video, 'jam': jam, 'bout': bout})


    def test_create_a_video_to_jam(self):
        v_to_j_dict = self._create_video_to_jam_data()
        data = {'video': v_to_j_dict['video'], 'jam': v_to_j_dict['jam']}
        v_to_j_serializer = VideoToJamSerializer()
        v_to_j = v_to_j_serializer.create(data)

        self.assertIsInstance(v_to_j, VideoToJam,
                msg="VideoToJamSerializer creating instance of incorrect class")

    def test_update_a_video_to_jam_time(self):
        v_to_j_dict = self._create_video_to_jam_data()
        first_start_time = '0m10s'
        first_end_time = '0m40s'
        updated_start_time = '5m5s'
        updated_end_time = '6m20s'
        data = {'video' : v_to_j_dict['video'], 'jam' : v_to_j_dict['jam'],
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
