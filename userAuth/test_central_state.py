from django.test import TestCase
from . import models

# add central as a state
class CentralState(TestCase):
    def test_central_state(self):
        state = models.TaxRates.objects.create(name="test", rate=0.1, isCentral=True)
        try:
            user = models.User.objects.create(
                username="test",
                state=state,
            )
            user.save()
            t = True
        except models.User.CentralAsStateException:
            t = False

        assert t == False
