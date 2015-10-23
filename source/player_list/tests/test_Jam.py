from django.test import TestCase

from player_list.models import Jam, Bout

class JamModelTest(TestCase):
	def test_jam_model_equality(self):
		bout = Bout.objects.create() 
		jam_1 = Jam.objects.create(bout=bout)
		jam_2 = Jam.objects.create(bout=bout)
#		print("jam 1: {0}\njam 2: {1}".format(jam_1, jam_2))
		self.assertEqual(jam_1, jam_2)

