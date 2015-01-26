from django.test import TestCase

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
