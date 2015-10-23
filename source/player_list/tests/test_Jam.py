from django.test import TestCase

from player_list.models import Jam, Bout

class JamModelTest(TestCase):
    def test_jam_str_formats_with_blank_optional_fields(self):
        bout = Bout.objects.create()
        jam = Jam.objects.create(bout=bout)
        jam_str = jam.__str__()
        self.assertEqual(jam_str, "id: {0}, {1}, Half #{2}, Jam #{3}".format(
            jam.id, jam.bout, jam.half, jam.number))
