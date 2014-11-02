from django.test import TestCase

from selenium import webdriver
from pyvirtualdisplay import Display

from player_list.views import view_bout_info

#Initial User Story
#Foo opens the a video_player to 

class BoutInfoTest(TestCase):

    def setUp(self):
        self.display = Display()
        self.display.start()

        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(10)

    def tearDown(self):
        self.browser.quit()
        self.display.stop()

    def test_WorkingTests(self):
        self.assert(True)

    def check_for_row_in_list_div(self, div_id, row_text):
        div = self.browser.find_element_by_id(div_id)
        self.assertIn(row_text, div, msg="{0} not found in div id {1}".format(
                                                             row_text, div_id))
