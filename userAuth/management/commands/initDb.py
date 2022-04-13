from django.core.management.base import BaseCommand
from userAuth.models import User
from userAuth.models import TaxRates
import random


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.count() == 0:
            # create admin
            # admin = User.objects.create_superuser(username="admin", password="admin")
            # admin.type = 3
            # admin.is_active = True
            # admin.is_admin = True
            # admin.save()

            # create states and their rates
            states = [
                "Andhra Pradesh",
                "Arunachal Pradesh",
                "Assam",
                "Bihar",
                "Chhattisgarh",
                "Goa",
                "Gujarat",
                "Haryana",
                "Himachal Pradesh",
                "Jharkhand",
                "Karnataka",
                "Kerala",
                "Madhya Pradesh",
                "Maharashtra",
                "Manipur",
                "Meghalaya",
                "Mizoram",
                "Nagaland",
                "Odisha",
                "Punjab",
                "Rajasthan",
                "Sikkim",
                "Tamil Nadu",
                "Telangana",
                "Tripura",
                "Uttar Pradesh",
                "Uttarakhand",
                "West Bengal",
            ]
            ut = [
                "Andaman and Nicobar Islands",
                "Chandigarh",
                "Dadra & Nagar Haveli and Daman & Diu",
                "Delhi",
                "Jammu and Kashmir",
                "Lakshadweep",
                "Puducherry",
                "Ladakh",
            ]
            TaxRates(
                name="Central",
                rate=(random.uniform(10, 20)),
                isUt=False,
                isCentral=True,
            ).save()

            for name in states:
                TaxRates(name=name, rate=(random.uniform(10, 20)), isUt=False).save()
            for name in ut:
                TaxRates(name=name, rate=(random.uniform(10, 20)), isUt=True).save()

        else:
            print("Admin accounts can only be initialized if no Accounts exist")
