from player_list.tests.test_Video import VideoTestCase

from django.http import HttpRequest
from django.core.urlresolvers import reverse

from WatchTape.views import home
from player_list.models import Video

class VideoListTest(VideoTestCase):
    def test_video_view_returns_correct_video(self):
        video = self._create_video()
        
        response = self.client.get(reverse("home"))
                
        self.assertTrue(isinstance(response.context['videos'], Video))
        self.assertEqual(response.context['videos'], video['instance'])