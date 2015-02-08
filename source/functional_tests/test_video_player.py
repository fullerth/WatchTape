from .base import FunctionalTest

from player_list.models import Video, Bout

class VideoPlayerTest(FunctionalTest):
    def test_video_player_title(self):
        video = Video()
        video.save()

        #Foo watches a video
        url = [self.server_url,
               '/video_player/video/{0}'.format(video.id),
               ]
        self.browser.get(''.join(url))

        #Foo sees the video_player page
        self.assertIn("Video of a Bout", self.browser.title)