from .base import FunctionalTest

from player_list.models import Video, Jam, VideoToJam, Bout

class VideoPlayerTest(FunctionalTest):
    def _create_video_player(self):
        video_player = {}
        video_player['bout'] = Bout()
        video_player['bout'].save()

        video_player['video'] = Video()
        video_player['video'].save()

        video_player['jam'] = Jam(bout=video_player['bout'])
        video_player['jam'].save()

        return video_player

    def test_video_player_title(self):
        video = self._create_video_player()['video']

        #Foo watches a video
        url = [self.server_url,
               '/video_player/video/{0}'.format(video.id),
               ]
        self.browser.get(''.join(url))

        #Foo sees the video_player page
        self.assertIn("Video of A Bout", self.browser.title)




