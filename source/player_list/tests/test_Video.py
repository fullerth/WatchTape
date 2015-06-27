from django.test import TestCase

from player_list.models import Video

from django.core.urlresolvers import reverse

class VideoTestCase(TestCase):
    def _create_video(self):
        expected_data = {'url':'http://foo.bar/', 'source':'fizz', 
                         'player_url':'asdf', 'site':'vimeo'}

        video = Video.objects.create(**expected_data)

        return {'instance': video, 'expected_data': expected_data}

class VideoTest(VideoTestCase):
    def test_video_created_with_defaults(self):
        video_dict = self._create_video()
        video_dict['instance'].full_clean()
        
    def test_video_has_get_absolute_url_method(self):
        video= self._create_video()['instance']
        url = video.get_absolute_url()
        
        self.assertEqual(url, 
                         reverse("video_player", kwargs={'video_id':video.id}))