from django.test import TestCase

from player_list.models import Bout

class BoutModelTest(TestCase):
	def test_bout_str_formats_with_blank_optional_fields(self):
		bout = Bout.objects.create()
		bout_str = bout.__str__()
		self.assertEqual(bout_str, "None vs None on {0}".format(bout.date))
