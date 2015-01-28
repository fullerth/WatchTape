from django.test import TestCase

import test_VideoToJam

from player_list.models import Bout

class test_BoutTest(TestCase):
    def test_bout_created_with_defaults(self):
        bout = Bout()
        bout.save()
