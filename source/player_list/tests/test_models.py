from django.test import TestCase

from player_list.models import VideoToJam, Video, Jam, Bout
from django.core.exceptions import ValidationError

class VideoToJamTest(TestCase):
    def create_video_to_jam(self, video_pk=1, bout_pk=1, jam_pk=1):
        data = {}
        data['video'] = Video.objects.create(pk=video_pk)
        data['bout'] = Bout.objects.create(pk=bout_pk)
        data['jam'] = Jam.objects.create(pk=jam_pk, bout=data['bout'])
        data['v_to_j'] = VideoToJam(video=data['video'], jam=data['jam'])
        return data
        
    def test_full_clean_only_requires_a_start_time(self):
        data = self.create_video_to_jam()
        try:
            data['v_to_j'].full_clean()
        except ValidationError as e:
            self.assertEqual(len(e.message_dict), 1, 
                'There should only be one field that raises a validation error')
            self.assertTrue('start_time' in e.message_dict, 
                'The validation error should be related to the start_time field')
            self.assertEqual(len(e.message_dict['start_time']), 1, 
                             'There should only be one error for start_time')
            self.assertEqual(e.message_dict['start_time'][0], 
                             'This field cannot be blank.',
                             'The start_time field error is not correct')

    def test_timecode_validator(self):
        data = self.create_video_to_jam()
        
        v_to_j = data['v_to_j']
        
        v_to_j._timecode_validator('0h5m10s')