from userAuth import factories
from django.core.management.base import BaseCommand
from userAuth import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        # create 10 of each using factories
        factories.TaxAccountantFactory.create_batch(10)
        factories.TaxFactory.create_batch(20)
        for x in models.TaxCalc.objects.order_by("?")[:5]:
            x.setPaid()
