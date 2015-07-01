from .base import FunctionalTest

from player_list.models import Video

class HomePageVideoList(FunctionalTest):
    def _create_video(self):
        video = Video.objects.create(site='vimeo', 
                                     player_url='http://localhost/',
                                     url='http://localhost/',
                                     source='foo')
        video_url = ''.join([self.server_url, video.get_absolute_url()])
        
        video_dict = {'instance':video, 'page_url':video_url}
        
        return video_dict
    
    def test_list_of_videos_exists(self):    
        video_dict = self._create_video()
        video = video_dict['instance']
        video_url = video_dict['page_url']
        
        self.browser.get(self.home_url)
        
        video_anchor = self.browser.find_element_by_id('id_videos'
                   ).find_element_by_xpath('.//ul//li//a')
        video_href = video_anchor.get_attribute('href')
        video_text = video_anchor.text
                   
        self.assertEqual(video_href, video_url)
        self.assertEqual(video_text, str(video))
        
    def test_two_videos_appear_in_list(self):
        expected_videos = [self._create_video(), self._create_video()]
        
        self.browser.get(self.home_url)
        
        videos = self.browser.find_element_by_id('id_videos'
                              ).find_elements_by_xpath('.//ul//li')
                              
        for idx, video in enumerate(videos):
            video_href = video.find_element_by_tag_name(
                                                    'a').get_attribute('href')
            self.assertEqual(expected_videos[idx]['page_url'], video_href, 
    msg="Video #{0} in list has incorrect href. Expected: {1}. Saw: {2}".format(
                        idx+1, expected_videos[idx]['page_url'], video_href))
            self.assertEqual(video.text, str(expected_videos[idx]['instance']))                 
        
        
        