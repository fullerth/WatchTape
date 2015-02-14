from django.test import TestCase, Client

import json

from rest_framework.renderers import JSONRenderer

from player_list.models import VideoToJam
from player_list.views import JSONResponse
from player_list.tests.test_VideoToJam import VideoToJamTestCase

class test_ViewVideoToJam(VideoToJamTestCase):
    def test_get_list_of_all_videotojams(self):
        c = Client()

        video_to_jam_1 = self._create_video_to_jam()
        video_to_jam_2 = self._create_video_to_jam()
        video_to_jam_1.save()
        video_to_jam_2.save()

        response = c.get('/watchtape/videotojam/')

        v_to_j_1_json = {'id' : video_to_jam_1.id,
                                               'video' : video_to_jam_1.video.id,
                                               'jam' : video_to_jam_1.jam.id,
                                               'start_time' : video_to_jam_1.start_time,
                                               'end_time' : video_to_jam_1.end_time}
        v_to_j_2_json = {'id' : video_to_jam_2.id,
                                               'video' : video_to_jam_2.video.id,
                                               'jam' : video_to_jam_2.jam.id,
                                               'start_time' : video_to_jam_2.start_time,
                                               'end_time' : video_to_jam_2.end_time}

        self.assertJSONEqual(response.content.decode(),
                             [v_to_j_1_json, v_to_j_2_json])

    def test_create_new_videotojam(self):
        c = Client()
        video_to_jam = self._create_video_to_jam()
        video_to_jam.start_time = '0h02m40s'
        video_to_jam.end_time = '1h8m60s'

        #Don't really like specifying the id here, but since this should
        #always be the first object created it should be OK
        data =  {  'id' : 1,
                   'video' : video_to_jam.video.id,
                   'jam' : video_to_jam.jam.id,
                   'start_time' : video_to_jam.start_time,
                   'end_time' : video_to_jam.end_time,
                }

        response = c.post('/watchtape/videotojam/',
                         json.dumps(data),
                         content_type='application/json')

        v_to_j = VideoToJam.objects.all()[0]
        self.assertEqual(v_to_j.start_time, data['start_time'],
                         msg="Start Time field incorrectly set in database")
        self.assertEqual(v_to_j.end_time, data['end_time'],
                         msg="End Timd field incorrectly set in database")


        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(response.content.decode(), data)



class test_ViewVideoToJamDetail(VideoToJamTestCase):
    def test_invalid_videoToJam_404(self):
        c = Client()

        response = c.get('/watchtape/videotojam/1/')

        self.assertEqual(response.status_code, 404)

    def test_get_videotojam_detail(self):
        c = Client()

        v_to_j = self._create_video_to_jam()
        v_to_j.save()

        response = c.get('/watchtape/videotojam/{0}/'.format(v_to_j.id))

        print(response.content)


class test_JsonResponse(TestCase):
    def test_returns_content_type_json(self):
        data = {}
        response = JSONResponse(data)

        expected_content_type = 'application/json'

        self.assertEqual(response['CONTENT-TYPE'], expected_content_type)

    def test_returns_json_formatted_data(self):
        data = {'one' : 1, 'two': 2}
        response = JSONResponse(data)

        self.assertEqual(response.content, JSONRenderer().render(data))
