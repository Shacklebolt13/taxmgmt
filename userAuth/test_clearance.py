from django.test import TestCase
from . import models

# lower clearance changes details of higher clearance


class ClearanceTest(TestCase):
    def test_clearance(self):
        passw = "test"
        uname = "test"

        user = models.User.objects.create(username=uname, user_type=1)
        user.set_password(passw)
        user.save()

        models.User.objects.create(username="tpayer", user_type=2).save()
        models.User.objects.create(username="adm", user_type=3).save()

        print(
            "logged In"
            if self.client.login(username=uname, password=passw)
            else "not logged in"
        )
        self.getUser()

    def getUser(self):
        resp = self.client.get("/api/users/")
        assert len(resp.data) == 1
