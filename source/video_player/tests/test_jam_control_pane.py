from django.test import TestCase

class JamControlTest(TestCase):
    def test_jam_control_view_uses_template(self):
        response = self.client.get(
            '/watchtape/video_player/controller/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video_player/controller.html')