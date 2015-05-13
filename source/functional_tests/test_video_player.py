from .base import FunctionalTest

from selenium.common.exceptions import NoSuchElementException

from player_list.models import Video, Jam, VideoToJam, Bout
from selenium.selenium import selenium

class VideoPlayerTest(FunctionalTest):
    class VideoPlayerPageFactory():
        def __init__(self, server_url, browser):
            self._create_new_video_player()
            self._get_video_page(server_url, browser)
            
        def _create_new_video_player(self):
            self.video_player = {}
            self.video_player['bout'] = Bout()
            self.video_player['bout'].save()
    
            self.video_player['video'] = Video()
            self.video_player['video'].save()
    
            self.video_player['jam'] = Jam(bout=self.video_player['bout'])
            self.video_player['jam'].save()

        def _get_video_page(self, server_url, browser):
            url = [server_url, 
                   '/watchtape/video_player/video/{0}'.format(
                                                self.video_player['video'].id),
                   ]
            browser.get(''.join(url))
            
            

    def test_video_player_title(self):
        '''Make sure that a video only, with no video_to_jams will display'''
        self.VideoPlayerPageFactory(self.server_url, self.browser)

        #Foo sees the video_player page
        self.assertIn("Video of A Bout", self.browser.title)

    def test_jam_list_appears(self):
        '''Test to make sure that the jam list appears in the correct tab'''
        self.VideoPlayerPageFactory(self.server_url, self.browser)        

        #There is a tab with jams displayed below the video
        jam_tab = self.browser.find_element_by_id('id_jam_time_tab')
        
        #Since there are no jams associated with this video the current data tab
        #does not appear
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('id_current_jam_tab')
        
        #A button is now visible in the jam tab to add jam times
        timing_button = jam_tab.find_element_by_id('id_jam_time_button')
        
        #The user clicks the button
        selenium.click(timing_button)
        
        #The jam is added to the database with the current video time
        
        #The jam appears in the jam tab under the jam list
        self.fail('finish the test!')

    