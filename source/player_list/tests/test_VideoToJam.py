from django.test import TestCase
from django.core.exceptions import ValidationError

from player_list.models import VideoToJam, Video, Jam, Bout


class test_VideoToJam(TestCase):

    def create_video_to_jam(self):
        #Create surrounding data
        video = Video()
        video.save()

        bout = Bout()
        bout.save()

        jam = Jam(bout=bout)
        jam.save()

        videotojam = VideoToJam(video=video, jam=jam)
        return videotojam


    def test_videotojam_created_with_defaults(self):
        video_to_jam = self.create_video_to_jam()
        video_to_jam.save()

        saved_v_to_j = VideoToJam.objects.all()[0]

        self.assertEqual(saved_v_to_j, video_to_jam)

    def test_videotojam_validation(self):
        video_to_jam = self.create_video_to_jam()

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
