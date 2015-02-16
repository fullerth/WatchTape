from django.test import TestCase, Client, RequestFactory

from video_player.factory import VideoPlayerFactory

import video_player.views

class test_VideoPlayer(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_uses_jam_timer_template_on_no_jam_times(self):
        '''
        Create a request with data that contains no videotojam items
        Verify that view_video_player renders the jam timing template
        in the response
        '''
        video_data = VideoPlayerFactory()

        request = self.request_factory.get('/video_player/video/{0}'.format(
                                    video_data.video.id))

        response = video_player.views.view_video_player(request,
                                                        video_data.video.id)

        self.assertTemplateUsed(response, 'stopwatch.html')
        self.assertTemplateNotUsed(response, 'stopwatch.html')
