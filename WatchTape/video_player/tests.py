from django.core.urlresolvers import resolve

from django.test import TestCase

from video_player.views import view_stopwatch
from player_list.models import Video

# Create your tests here.
class StopwatchViewTest(TestCase):
    def test_page_root(self):
        found = resolve('/watchtape/video_player/stopwatch/1/')
        self.assertEqual(found.func, view_stopwatch)

    def test_uses_stopwatch_template(self):
        video = Video.objects.create()
        response = self.client.get('/watchtape/video_player/stopwatch/{0}/'.format(
                                        video.id))
        self.assertTemplateUsed(response, 'video_player/stopwatch.html')

    def test_jam_button_prints_time(self):
        video = Video.objects.create()
        response = self.client.get('/watchtape/video_player/stopwatch/{0}/'.format(
                                        video.id))

        self.assertContains
