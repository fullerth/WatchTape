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

        #Foo sees the info starts at jam 1

        #Foo sees the next jam control on the page
        next_jam = self.browser.find_element_by_id('id_next_jam')

        #Foo presses the next jam control

        #The data for the next jam is displayed

        self.fail('finish the test')