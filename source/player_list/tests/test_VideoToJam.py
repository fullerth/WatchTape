from django.test import TestCase
from django.core.exceptions import ValidationError

from player_list.models import VideoToJam, Video, Jam, Bout

import unittest

class VideoToJamTestCase(TestCase):
    def _create_video_to_jam(self):
        #Create surrounding data
        video = Video()
        video.save()

        bout = Bout()
        bout.save()

        jam = Jam(bout=bout)
        jam.save()

        videotojam = VideoToJam(video=video, jam=jam)
        return videotojam


class test_VideoToJam(VideoToJamTestCase):

    @unittest.skip("Timecode URL generation not currently used, remove if not needed")
    def test_videotojam_returns_url(self):
        video_to_jam = self._create_video_to_jam()
        jam_start_time = "2m60s"
        video_url = "http://test/video"
        jam_url = ''.join([video_url, "#t=", jam_start_time])

        video_to_jam.start_time = jam_start_time
        video_to_jam.video.url = video_url
        video_to_jam.video.save()
        video_to_jam.save()

        self.assertEqual(video_to_jam.timecode_url, jam_url)
