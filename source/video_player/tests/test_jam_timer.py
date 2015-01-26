from django.test import TestCase

from player_list.models import Bout

class JamTimerTester(TestCase):

    def test_jam_timer_view_uses_template(self):
        bout = Bout.objects.create()

        response = self.client.get(
            '/video_player/jam_timer/bout/{0}/'.format(bout.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video_player/stopwatch.html')