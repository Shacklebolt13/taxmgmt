from django.test import TestCase
from . import models

# add mutltiple centrals
class MultipleCentralTest(TestCase):
    def test_multiple_central(self):

        try:
            models.TaxRates.objects.create(name="test", rate=0.1, isCentral=True).save()
            models.TaxRates.objects.create(name="test", rate=0.1, isCentral=True).save()
            t = True
        except:
            t = False

        assert t == False
