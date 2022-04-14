from django.forms import ModelForm
from . import models


class createUserForm(ModelForm):
    class Meta:
        model = models.User
        fields = ["username", "user_type", "state"]


class createTaxForm(ModelForm):
    class Meta:
        model = models.TaxCalc
        fields = [
            "baseIncome",
            "allowance",
            "taxable_prereq",
            "income_from_property",
            "st_cap_gain_immovable",
            "lt_cap_gain_immovable",
            "pan",
        ]
