from player_list.tests.test_Video import VideoTestCase

from django.http import HttpRequest
from django.core.urlresolvers import reverse

from WatchTape.views import home
from player_list.models import Video

class VideoListTest(VideoTestCase):
    def test_home_page_context_contains_correct_videos(self):
        video_1 = self._create_video()
        video_2 = self._create_video()
        
        videos = [video_1, video_2]
        
        response = self.client.get(reverse("home"))
                
        for i, video in enumerate(response.context['videos']):
            self.assertTrue(isinstance(video, Video))
            self.assertEqual(video, videos[i]['instance'])