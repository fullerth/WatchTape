import json

from django.test import TestCase, Client

from player_list.models import VideoToJam, Video, Jam, Bout, _timecode_validator
from django.core.exceptions import ValidationError

from rest_framework import status

class VideoToJamTestCase(TestCase):
    def _create_video_to_jam(self, video_pk=None, bout_pk=None, jam_pk=None):
        data = {}
        data['video'] = Video.objects.create(pk=video_pk)
        data['bout'] = Bout.objects.create(pk=bout_pk)
        data['jam'] = Jam.objects.create(pk=jam_pk, bout=data['bout'])
        data['v_to_j'] = VideoToJam(video=data['video'], jam=data['jam'])
        return data

class VideoToJamModelTest(VideoToJamTestCase):
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
            _timecode_validator(timecode)
        
    def test_timecode_validator_with_invalid_timecodes(self):
        data = self._create_video_to_jam()
        
        v_to_j = data['v_to_j']
        
        invalid_timecodes = ['foo', '', '22z15h18s', '7h4m3ss']
        for timecode in invalid_timecodes:
            with self.assertRaises(ValidationError):
                _timecode_validator(timecode)

class VideoToJamViewTests(VideoToJamTestCase): 
    def test_videotojam_list_exists(self):
        c = Client()
        response = c.get('/watchtape/videotojam/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK, 
            msg="video_to_jam list does not exist")
    
    def test_get_list_of_all_videotojams(self):
        c = Client()
        
        video_to_jam_1 = self._create_video_to_jam()['v_to_j']
        video_to_jam_2 = self._create_video_to_jam()['v_to_j']
        video_to_jam_1.save()
        video_to_jam_2.save()
        
        response = c.get('/watchtape/videotojam/')
        
        v_to_j_1_json = { 'id' : video_to_jam_1.id,
                          'video' : video_to_jam_1.video.id,
                          'jam' : video_to_jam_1.jam.id,
                          'start_time' : video_to_jam_1.start_time,
                          'end_time' : video_to_jam_1.end_time,
                          'timecode_url' : video_to_jam_1.timecode_url
                        }
        
        v_to_j_2_json = { 'id' : video_to_jam_2.id,
                          'video' : video_to_jam_2.video.id,
                          'jam' : video_to_jam_2.jam.id,
                          'start_time' : video_to_jam_2.start_time,
                          'end_time' : video_to_jam_2.end_time,
                          'timecode_url' : video_to_jam_2.timecode_url
                        }
        expected_json = [v_to_j_1_json, v_to_j_2_json]
        
        self.assertJSONEqual(response.content.decode(), expected_json,
            msg="GET /watchtape/videotojam/ did not produce expected JSON")
    
    def test_invalid_post_reports_bad_request_code(self):
        c = Client()
        
        response = c.post('/watchtape/videotojam/')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            msg="POST to /watchtape/videotojam/ with invalid data did not \
produce the expected error code")
        
    def test_invalid_post_reports_error_message(self):
        c = Client()
                
        response = c.post('/watchtape/videotojam/')
        
        expected_response = {"start_time":["This field is required."],
                             "jam":["This field is required."],
                             "video":["This field is required."]}
        
        self.assertJSONEqual(response.content.decode(), expected_response,
            msg="POST to /watchtape/videotojam/ with invalid data did not \
produce the expected error code.")
    
    def test_valid_post_returns_201_CREATED_status_code(self):
        c = Client()
        
        video_to_jam_1 = self._create_video_to_jam()['v_to_j']
        
        video_to_jam_1.start_time = "1m42s"
        
        v_to_j_1_json = { 'id' : video_to_jam_1.id,
                          'video' : video_to_jam_1.video.id,
                          'jam' : video_to_jam_1.jam.id,
                          'start_time' : video_to_jam_1.start_time,
                          'end_time' : video_to_jam_1.end_time,
                          'timecode_url' : video_to_jam_1.timecode_url
                        }
        
        response = c.post('/watchtape/videotojam/', v_to_j_1_json)    

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            msg="API did not create an object for POST to /watchtape/videotojam")
        
    def test_valid_post_returns_expected_JSON(self):
        c = Client()
        
        video_to_jam_1 = self._create_video_to_jam()['v_to_j']
        
        video_to_jam_1.start_time = "1m42s"
        
        v_to_j_1_json = { 'id' : video_to_jam_1.id,
                          'video' : video_to_jam_1.video.id,
                          'jam' : video_to_jam_1.jam.id,
                          'start_time' : video_to_jam_1.start_time,
                          'end_time' : video_to_jam_1.end_time,
                          'timecode_url' : video_to_jam_1.timecode_url
                        }
        
        response = c.post('/watchtape/videotojam/', v_to_j_1_json)    

        #The post should save the video to jam to the database and it should be
        #the only row in the table
        v_to_j_1_json['id'] = 1
        
        self.assertJSONEqual(response.content.decode(), v_to_j_1_json, 
            msg="unexpected json response from POST to /watchtape/videotojam")
