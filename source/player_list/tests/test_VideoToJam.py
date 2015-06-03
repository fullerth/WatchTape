from django.test import TestCase

from player_list.models import VideoToJam, Video, Jam, Bout
from django.core.exceptions import ValidationError

class VideoToJamTest(TestCase):
    def _create_video_to_jam(self, video_pk=1, bout_pk=1, jam_pk=1):
        data = {}
        data['video'] = Video.objects.create(pk=video_pk)
        data['bout'] = Bout.objects.create(pk=bout_pk)
        data['jam'] = Jam.objects.create(pk=jam_pk, bout=data['bout'])
        data['v_to_j'] = VideoToJam(video=data['video'], jam=data['jam'])
        return data
    
    def test_videotojam_created_with_defaults(self):
        data = self._create_video_to_jam()
        data['v_to_j'].save()

        saved_v_to_j = VideoToJam.objects.all()[0]

        self.assertEqual(saved_v_to_j, data['v_to_j'])

    def test_videotojam_start_seconds(self):
        video_to_jam = self._create_video_to_jam()['v_to_j']

        #Test start seconds (5h10m8s = 18608 seconds)
        video_to_jam.start_time = "5h10m8s"

        self.assertEqual(video_to_jam.start_seconds, 18608)
    
    def test_full_clean_only_requires_a_start_time(self):
        data = self._create_video_to_jam()
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

    def test_timecode_validator_with_valid_timecodes(self):
        data = self._create_video_to_jam()
        
        v_to_j = data['v_to_j']
        
        #Check that this list of valid timecodes do not raise exceptions
        valid_timecodes = ['0h5m10s', 
                           '3h18s', '6h4m', '8m55s', 
                           '5h', '13m', '2s', ]
        for timecode in valid_timecodes:
            v_to_j._timecode_validator(timecode)
        
    def test_timecode_validator_with_invalid_timecodes(self):
        data = self._create_video_to_jam()
        
        v_to_j = data['v_to_j']
        
        invalid_timecodes = ['foo', '', '22z15h18s', '7h4m3ss']
        for timecode in invalid_timecodes:
            with self.assertRaises(ValidationError):
                v_to_j._timecode_validator(timecode)
                