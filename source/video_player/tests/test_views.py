from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse

from video_player.views import view_video_player
from player_list.models import Video, Bout, Jam, VideoToJam, Roster, Team, Player, PlayerToRoster

class VideoTaggingTests(TestCase):
	def setUp(self):
		self.video = Video.objects.create()
		self.video.save()
	
	def _add_player(self):
		player = Player.objects.create()
		player.save()
		return player

	def _add_bout(self, video):
		home_team = Team.objects.create()
		away_team = Team.objects.create()
		home_roster = Roster.objects.create(team=home_team)
		away_roster = Roster.objects.create(team=away_team)

		bout = Bout.objects.create(home_roster=home_roster, 
				away_roster=away_roster)
		bout.save()
		jam = Jam.objects.create(bout=bout)
		jam.save()
		video_to_jam = VideoToJam.objects.create(video=video,
												 jam=jam)
		video_to_jam.start_time='0h0m2s'
		video_to_jam.save()

		return{'home_roster':home_roster, 'away_roster':away_roster, 'jam':jam}
	

	def test_video_player_renders_with_malformed_database(self):
		request = RequestFactory()
		request.get(reverse('video_player', kwargs={'video_id':1}))
		response = view_video_player(request, 1)
		self.assertEqual(response.status_code, 200)

	def test_video_player_renders_with_empty_rosters(self):
		self._add_bout(self.video)
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)

	def test_video_player_context_contains_jams_in_one_bout(self):
		bout_info = self._add_bout(self.video)
		response = self.client.get('/')
		jam_list = map(repr, [bout_info['jam']])
		self.assertQuerysetEqual(response.context['jams'], jam_list) 

	def test_video_player_context_contains_jams_in_two_bouts(self):
		bout_1_info = self._add_bout(self.video)
		bout_2_info = self._add_bout(self.video)
		response = self.client.get('/')
		jam_list = map(repr, [bout_1_info['jam'], bout_2_info['jam']])
		self.assertQuerysetEqual(response.context['jams'], jam_list,
			ordered=False)
		
