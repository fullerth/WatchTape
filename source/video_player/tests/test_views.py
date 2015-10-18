from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse

from video_player.views import view_video_player
from player_list.models import Video, Bout, Jam, VideoToJam

class VideoTaggingTests(TestCase):
	def setUp(self):
		self.video = Video.objects.create()
		self.video.save()
	
	def _add_a_bout(self, video):
		bout = Bout.objects.create()
		bout.save()
		jam = Jam.objects.create(bout=bout)
		jam.save()
		video_to_jam = VideoToJam.objects.create(video=self.video,
												 jam=jam)
		video_to_jam.start_time='0h0m2s'
		video_to_jam.save()

	def test_video_player_works_with_malformed_database(self):
		request = RequestFactory()
		request.get(reverse('video_player', kwargs={'video_id':1}))
		response = view_video_player(request, 1)
		self.assertEqual(response.status_code, 200)

	def test_video_player_selects_single_jams(self):
		self._add_a_bout(self.video)
		response = self.client.get('/')
		print(response.context['times'])
		self.assertEqual(response.status_code, 200)
		self.fail()
