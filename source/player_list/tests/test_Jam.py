from django.test import TestCase

from player_list.models import Jam, Bout

class JamModelTest(TestCase):
	def test_jam_model_equality(self):
		bout = Bout.objects.create() 
		jam_1 = Jam.objects.create(bout=bout)
		jam_2 = Jam.objects.create(bout=bout)
		self.assertEqual(jam_1, jam_2)

	def test_jam_str_formats_with_blank_optional_fields(self):
		bout = Bout.objects.create()
		jam = Jam.objects.create(bout=bout)
		jam.__str__()
