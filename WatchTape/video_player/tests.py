from django.core.urlresolvers import resolve

from django.test import TestCase

from video_player.views import view_stopwatch

# Create your tests here.
class StopwatchViewTest(TestCase):
    def test_page_root(self):
        found = resolve('/watchtape/video_player/stopwatch/1/')
        self.assertEqual(found.func, view_stopwatch)