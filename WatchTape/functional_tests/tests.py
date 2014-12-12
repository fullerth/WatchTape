import os
import sys
from datetime import datetime

from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from pyvirtualdisplay import Display

class JamStopwatchTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if not self._outcomeForDoCleanups.success:
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to_window(handle)
                self.take_screenshot()
                self.dump_html()
        self.browser.quit()
        self.display.stop()

    def setUp(self):
        self.display = Display()
        self.display.start()

        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(10)

    def take_screenshot(self):
        filename = self._get_filename() + '.png'
        print('screenshotting to', filename)
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        filename = self._get_filename() + '.html'
        print('dumping page HTL to', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.format(
            folder = SCREEN_DUMP_LOCATION,
            classname = self.__class__.__name__,
            method = self._testMethodName,
            windowid = self._windowid,
            timestamp=timestamp
        )


    def test_jam_stopwatch_exists_and_records_times(self):
        # The protagonist opens a browser
        self.browser.get(self.server_url + 'watchtape/video_player/stopwatch/1')

        # They notice the page title and are presented with a video and a button
        assert 'Stopwatch' in self.browser.title
        header_text = self.browser.find_element_by_id('id_jam_start')

        # Fingers may twiddle as the video buffers before it auto starts
        self.fail('Finish the test!')

        # The video plays, the faint clatter of skates through tiny speakers
        # Filters into the room

        # A jam ends and the protagonists finger presses the button

        # A tally of the current time is displayed

        # The video continues to play

        # Another jam ends and the button is clicked

        # Both times are displayed

