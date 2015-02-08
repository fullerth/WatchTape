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
    def test_videotojam_created_with_defaults(self):
        video_to_jam = self._create_video_to_jam()
        video_to_jam.save()

        saved_v_to_j = VideoToJam.objects.all()[0]

        self.assertEqual(saved_v_to_j, video_to_jam)

    def test_videotojam_validation(self):
        video_to_jam = self._create_video_to_jam()

        #Test start_time validation
        video_to_jam.start_time = "foo"
        with self.assertRaises(ValidationError):
            video_to_jam.clean_fields(exclude=["end_time", "timecode_url"])
        video_to_jam.start_time = "4h245m60s"
        video_to_jam.clean_fields(exclude=["end_time", "timecode_url"])

        #Test end_time validation
        video_to_jam.end_time = "bar"
        with self.assertRaises(ValidationError):
            video_to_jam.clean_fields(exclude=["start_time", "timecode_url"])
        video_to_jam.end_time = "16h18m320s"
        video_to_jam.clean_fields(exclude=["start_time", "timecode_url"])

    def test_videotojam_start_seconds(self):
        video_to_jam = self._create_video_to_jam()

        #Test start seconds (5h10m8s = 18608 seconds)
        video_to_jam.start_time = "5h10m8s"

        self.assertEqual(video_to_jam.start_seconds, 18608)

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
