from .base import FunctionalTest

from selenium.common.exceptions import NoSuchElementException

from player_list.models import Video, Jam, VideoToJam, Bout

class VideoPlayerTest(FunctionalTest):
    def _create_video_player(self):
        video_player = {}
        video_player['bout'] = Bout()
        video_player['bout'].save()

        video_player['video'] = Video()
        video_player['video'].save()

        video_player['jam'] = Jam(bout=video_player['bout'])
        video_player['jam'].save()

        return video_player

    def test_video_player_title(self):
        '''Test to make sure that a video only, with no video_to_jams will display'''
        video = self._create_video_player()['video']

        #Foo watches a video
        url = [self.server_url,
               '/watchtape/video_player/video/{0}'.format(video.id),
               ]
        self.browser.get(''.join(url))

        #Foo sees the video_player page
        self.assertIn("Video of A Bout", self.browser.title)

    def test_jam_list_appears(self):
        '''Test to make sure that the jam list appears in the correct tab'''
        video_player = self._create_video_player()

        #Foo watches a video
        url = [self.server_url,
               '/video_player/video/{0}'.format(video_player['video'].id),
               ]
        self.browser.get(''.join(url))

        #There is a tab with jams displayed below the video
        jam_tab = self.browser.find_element_by_id('id_jam_time_tab')
        
        #Since there are no jams associated with this video the current data tab
        #does not appear
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('id_id_current_jam_tab')
        
        #A button is now visible in the jam tab to add jam times
        timing_button = jam_tab.find_element_by_id('id_jam_time_button')
        
        #The user clicks the button
        
        #The jam is added to the database with the current video time
        
        #The jam appears in the jam tab under the jam list
        self.fail('finish the test!')

    