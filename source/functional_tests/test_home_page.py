from .base import FunctionalTest

from player_list.models import Video

from django.core.urlresolvers import reverse


class HomePageVideoList(FunctionalTest):
    def test_list_of_videos_exists(self):        
        video = Video.objects.create(site='vimeo', 
                                     player_url='http://localhost/',
                                     url='http://localhost/',
                                     source='foo')
        video_url = video.get_absolute_url()
        self.browser.get(video_url)
        
        video_anchor = self.browser.find_element_by_id('id_videos'
                   ).find_element_by_xpath('.//li//a')
        video_href = video_anchor.get_attribute('href')
        video_text = video_anchor.text
        print(video_text)
                   
        self.assertEqual(video_href, video_url)
        self.assertEqual(video_text, str(video))
        