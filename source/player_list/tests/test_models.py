from django.test import TestCase

from player_list.models import Bout

class BoutTest(TestCase):
    def test_bout_created_with_defaults(self):
        bout = Bout()
        bout.save()
