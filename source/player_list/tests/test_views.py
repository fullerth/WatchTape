from django.test import TestCase, Client

from rest_framework.renderers import JSONRenderer

from player_list.models import VideoToJam
from player_list.views import JSONResponse
from player_list.tests.test_VideoToJam import VideoToJamTestCase

class test_ViewVideoToJam(VideoToJamTestCase):
    def test_get_list_of_all_videotojams(self):
        c = Client()

        video_to_jam_1 = self._create_video_to_jam()
        video_to_jam_2 = self._create_video_to_jam()

        response = c.get('/videotojam/')

        print(response.content)

        self.assertContains(response.content, video_to_jam_1)
        self.assertContains(response.content, video_to_jam_2)


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
