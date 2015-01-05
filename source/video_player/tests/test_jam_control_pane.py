from django.test import TestCase

class JamControlTest(TestCase):
    def test_jam_control_view_exists(self):
        self.client.get(
            '/video_player/controller')