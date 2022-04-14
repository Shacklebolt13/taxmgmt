from tabnanny import verbose
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

import pytz

states = [
    ("Andhra Pradesh", "Andhra Pradesh"),
    ("Arunachal Pradesh", "Arunachal Pradesh"),
    ("Assam", "Assam"),
    ("Bihar", "Bihar"),
    ("Chhattisgarh", "Chhattisgarh"),
    ("Goa", "Goa"),
    ("Gujarat", "Gujarat"),
    ("Haryana", "Haryana"),
    ("Himachal Pradesh", "Himachal Pradesh"),
    ("Jharkhand", "Jharkhand"),
    ("Karnataka", "Karnataka"),
    ("Kerala", "Kerala"),
    ("Madhya Pradesh", "Madhya Pradesh"),
    ("Maharashtra", "Maharashtra"),
    ("Manipur", "Manipur"),
    ("Meghalaya", "Meghalaya"),
    ("Mizoram", "Mizoram"),
    ("Nagaland", "Nagaland"),
    ("Odisha", "Odisha"),
    ("Punjab", "Punjab"),
    ("Rajasthan", "Rajasthan"),
    ("Sikkim", "Sikkim"),
    ("Tamil Nadu", "Tamil Nadu"),
    ("Telangana", "Telangana"),
    ("Tripura", "Tripura"),
    ("Uttar Pradesh", "Uttar Pradesh"),
    ("Uttarakhand", "Uttarakhand"),
    ("West Bengal", "West Bengal"),
]

ut = [
    ("Andaman and Nicobar Islands", "Andaman and Nicobar Islands"),
    ("Chandigarh", "Chandigarh"),
    ("Dadra & Nagar Haveli and Daman & Diu", "Dadra & Nagar Haveli and Daman & Diu"),
    ("Delhi", "Delhi"),
    ("Jammu and Kashmir", "Jammu and Kashmir"),
    ("Lakshadweep", "Lakshadweep"),
    ("Puducherry", "Puducherry"),
    ("Ladakh", "Ladakh"),
]


class User(AbstractUser):
    class NotEnoughClearanceException(Exception):
        pass

    types = ((1, "TaxPayer"), (2, "TaxAccountant"), (3, "Admin"))
    user_type = models.IntegerField(choices=types, default=1)
    state = models.ForeignKey("userAuth.taxrates", on_delete=models.CASCADE, null=True)

    def save(self, clearance=1, *args, **kwargs):
        print(args, kwargs)
        uf = kwargs.get("update_fields")
        if uf is not None and not (len(uf) == 1 and uf[0] == "last_login"):
            if self.user_type > clearance:
                raise self.NotEnoughClearanceException(
                    "You don't have enough clearance to do this"
                )

        super(User, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.get_full_name() or self.username


class TaxRates(models.Model):
    class Meta:
        verbose_name_plural = "State/UT Tax Rates"

    class DuplicateCentralError(Exception):
        pass

    name = models.CharField(max_length=100)
    rate = models.FloatField(max_length=100)
    isUt = models.BooleanField(default=False)
    isCentral = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.isCentral and TaxRates.objects.filter(isCentral=True).exists():
            raise self.DuplicateCentralError("You can`t add another Central")
        return super(TaxRates, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}--{self.rate:0.1f}"


# uses https://taxsummaries.pwc.com/india/individual/sample-personal-income-tax-calculation
# instead of surcharge, I add gst to the final income tax.
# and removed the health tax etc.
# this is just a rough estimate, and will be updated as and when required.


class TaxCalc(models.Model):
    class Meta:
        verbose_name_plural = "Users' Taxes"

    class AlreadyPaidException(Exception):
        pass

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    baseIncome = models.FloatField()
    allowance = models.FloatField()
    taxable_prereq = models.FloatField()
    income_from_property = models.FloatField()
    st_cap_gain_immovable = models.FloatField()
    lt_cap_gain_immovable = models.FloatField()
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    paid_on = models.DateTimeField(null=True, blank=True, editable=False)
    due_on = models.DateTimeField(blank=True, null=True, editable=False)
    finalAmt = models.FloatField(default=0, editable=False)
    pan = models.CharField(max_length=15)

    @property
    def paid(self):
        if self.paid_on is not None:
            return True
        else:
            return False

    @property
    def total_taxable_income(self):
        return (
            self.baseIncome
            + self.allowance
            + self.taxable_prereq
            + self.income_from_property
            + self.st_cap_gain_immovable
            + self.lt_cap_gain_immovable
        )

    @property
    def _subtotal_tax(self):
        temp = self.total_taxable_income - self.lt_cap_gain_immovable
        tp = 0
        if temp > 250001 and temp <= 500000:
            tp = 5
        elif temp > 500001 and temp <= 1000000:
            tp = 20
        else:
            tp = 30

        return tp * temp / 100

    @property
    def _total_tax(self):
        tmp = self._subtotal_tax
        return (0.02 * self.lt_cap_gain_immovable) + tmp

    @property
    def gst(self):
        return self.user.state.rate + TaxRates.objects.get(isCentral=True).rate

    @property
    def total_tax(self):
        tot = self._total_tax
        tot += tot * self.gst / 100
        return tot

    def save(self, paid_now=False, *args, **kwargs):
        print(kwargs)
        self.finalAmt = self.total_tax
        if not paid_now:
            if self.paid_on is not None:
                raise self.AlreadyPaidException(
                    "The User Has Already Paid the Tax, It can`t be edited anymore"
                )

        self.due_on = (
            self.updated_on
            or datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        ) + datetime.timedelta(days=30)

        return super(TaxCalc, self).save(*args, **kwargs)

    def setPaid(self):
        self.paid_on = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        self.save(paid_now=True)
