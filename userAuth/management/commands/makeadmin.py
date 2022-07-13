from django.core.management.base import BaseCommand
from userAuth import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        # create 10 of each using factories
        user = models.User.objects.create_superuser("admin", "admin", "admin")
        user.user_type = 3
        # user.state = models.TaxRates.objects.order_by("?")[0]
        user.save(clrnce=3)
