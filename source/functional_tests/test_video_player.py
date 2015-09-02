from .base import FunctionalTest

from selenium.common.exceptions import NoSuchElementException

from django.test.utils import override_settings

from player_list.models import Video, Jam, VideoToJam, Bout
from selenium.selenium import selenium

class VideoPlayerTest(FunctionalTest):
    class VideoPlayerPageFactory():
        def __init__(self, server_url, browser, create_jam_times=False, 
                     get_page=True):
            self._create_new_video_player()
            if(create_jam_times):
                self._create_video_to_jams()
            if(get_page):
                self.get_video_page(server_url, browser)

        def _create_new_video_player(self):
            self.video_player = {}
            self.video_player['bout'] = Bout()
            self.video_player['bout'].save()

            self.video_player['video'] = Video()
            self.video_player['video'].save()

            self.video_player['jam'] = Jam(bout=self.video_player['bout'])
            self.video_player['jam'].save()

        def get_video_page(self, server_url, browser):
            url = [server_url,
                   '/watchtape/video_player/video/{0}'.format(
                                                self.video_player['video'].id),
                   ]
            browser.get(''.join(url))

        def _create_video_to_jams(self):
            self.video_player['video_to_jam'] = VideoToJam(
                                            video=self.video_player['video'],
                                            start_time="1m0s")
            self.video_player['video_to_jam'].full_clean()         
            self.video_player['video_to_jam'].save()
            

    def test_video_player_title(self):
        '''Make sure that a video only, with no video_to_jams will display'''
        self.VideoPlayerPageFactory(self.server_url, self.browser)

        #Foo sees the video_player page
        self.assertIn("Video of A Bout", self.browser.title)

    def test_jam_list_appears(self):
        '''Test to make sure that the jam list appears in the correct tab'''
        self.VideoPlayerPageFactory(self.server_url, self.browser)

        #There is a tab with jams displayed below the video
        self.browser.find_element_by_id('id_jam_time_tab')
        jam_time_data = self.browser.find_element_by_id('id_jam_list_tab')

        #Since there are no jams associated with this video the current data tab
        #does not appear
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('id_current_jam_tab')

        #A button is now visible in the jam tab to add jam times
        timing_button = self.browser.find_element_by_id('id_jam_time_button')

        #The user clicks the button
        timing_button.click()

        #The jam is added to the database with the current video time
        #This data is then displayed in the list of jams in the jam data tab
        jam_times = jam_time_data.find_elements_by_tag_name('li')
        
        #There should be one and only one jam in the list
        self.assertEqual(len(jam_times), 1, 
                         "There should be one and only one jam time in the list")

        #The jam appears in the jam tab under the jam list
        self.fail('finish the test!')

    def test_video_player_renders_with_no_video(self):
        '''Test to make sure that lack of a video URL does not cause rendering problems'''
        self.VideoPlayerPageFactory(self.server_url, self.browser)

        #Not rendering the vimeo_player with no src url is a valid solution to 
        #this issue
        try:
            vimeo_player = self.browser.find_element_by_id('id_vimeo_player')
        except NoSuchElementException:
            return

        #Should never point to localhost, but it may if a malformed relative
        #url is created for the src attribute
        self.assertNotIn("localhost", vimeo_player.get_attribute("src"),
            "video.player_url was not specified and the template did not handle \
 it gracefully")
       
    def test_tabs_display_content(self):
        '''Test to make sure that the navigation tabs are functional'''
        self.VideoPlayerPageFactory(self.server_url, self.browser, 
                                    create_jam_times=True)
        
        tabs = self.browser.find_elements_by_xpath(
            "//div[@id='id_navigation_tabs']/ul/li")
        
        for tab in tabs:
            tab.click()
            self.fail('figure out how to test tab contents are shown')
        