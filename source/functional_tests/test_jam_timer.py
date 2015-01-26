from .base import FunctionalTest

from player_list.models import Bout

class JamTimerTest(FunctionalTest):
    def setUp(self):
        return (super(JamTimerTest, self).setUp())

    def test_jam_timer_page(self):
        bout = Bout()
        bout.save()

        #Foo gets a list of all the current jam times for the bout
        url = [self.server_url,
               '/video_player/jam_timer/bout/{0}'.format(bout.id),
              ]
        self.browser.get(''.join(url))

        #Foo sees that the jam times for the current jam are displayed
        self.browser.find_element_by_id('id_jam_time_list')

        self.fail('finish the test')