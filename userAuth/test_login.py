from django.test import TestCase
from . import models

# Create your tests here.

# Test login
class LoginTest(TestCase):
    def test_login(self):
        uname = "test"
        passw = "test"
        user = models.User.objects.create(username=uname)
        user.set_password("test")
        user.save()

        response = self.client.post(
            "/api/auth/", {"username": uname, "password": passw}
        )

        self.assertEqual(response.status_code, 200)


# lower clearance changes details of higher clearance
