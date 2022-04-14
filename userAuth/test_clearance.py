from django.test import TestCase
from . import models

# lower clearance changes details of higher clearance


class ClearanceTest(TestCase):
    def test_clearance(self):
        self.client.user = models.User.objects.create(username="test", user_type=1)
        self.client.login()
