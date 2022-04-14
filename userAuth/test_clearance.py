from django.test import TestCase
from . import models

# lower clearance changes details of higher clearance


class ClearanceTest(TestCase):
    def test_clearance(self):
        self.passw = "test"
        self.uname = "test"

        models.User(username="tpayer", user_type=2).save(clrnce=3)
        models.User(username="adm", user_type=3).save(clrnce=3)

        self.getUserLow()
        self.userClearanceUpgrade()
        self.getUserHigh()

    def getUserLow(self):

        user = models.User(username=self.uname, user_type=1)
        user.set_password(self.passw)
        user.save()

        self.user = user

        assert self.client.login(username=self.uname, password=self.passw) == True

        resp = self.client.get("/api/users/")
        assert len(resp.data) == 1

    def userClearanceUpgrade(self):

        self.user.user_type = 3
        try:
            self.user.save()
            t = True
        except:
            t = False

        assert t == False

    def getUserHigh(self):

        self.user_type = 3
        self.user.save(clrnce=3)

        assert self.client.login(username=self.uname, password=self.passw) == True

        resp = self.client.get("/api/users/")
        assert len(resp.data) > 1
