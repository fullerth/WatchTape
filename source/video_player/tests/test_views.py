from django.test import TestCase, RequestFactory

from video_player.views import view_video_player
from player_list.models import Video

class VideoTaggingTests(TestCase):
    def setUp(self):
        self.requestFactory = RequestFactory()
        
    def test_renders_page_without_any_video_to_jams(self):
        video = Video()
        video.save()
        
        request = self.requestFactory.get('/video_player/video/{0}'.format(
                                                                    video.id))
        
        response = view_video_player(request, video.id)
        
        self.assertEqual(response.status_code, 200, 
                         "Failed to load video player page")
        
        return response