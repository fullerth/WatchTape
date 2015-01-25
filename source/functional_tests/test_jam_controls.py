from .base import FunctionalTest

from player_list.models import Bout

class JamControlsTest(FunctionalTest):
    def setUp(self):
        super(JamControlsTest, self).setUp()
        self.bout = Bout()
        self.bout.save()

    def test_jam_controls_page(self):
        #Foo brings up a jam control panel
        url = [self.server_url,
               '/watchtape/video_player/controller/']
        self.browser.get(''.join(url))

        #Foo sees the jam controls on the page
        next_jam = self.browser.find_element_by_id('id_next_jam')
        prev_jam = self.browser.find_element_by_id('id_prev_jam')


        #Foo sees the info starts at jam 1
        current_jam = self.browser.find_element_by_id('id_current_jam')
        expected_jam = 1
        self.assertEquals(current_jam.text, 'Jam {0}'.format(expected_jam))

        #Foo presses next and prev controls and verifies current jam changes

        self.fail('finish the test')