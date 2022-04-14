from pyexpat import model
import factory
from . import models
import random


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User
        django_get_or_create = ("username",)

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("user_name")

    @factory.lazy_attribute
    def state(self):
        return models.TaxRates.objects.get(pk=random.randint(2, 28))


class TaxPayerFactory(UserFactory):

    user_type = 1


class TaxAccountantFactory(UserFactory):

    user_type = 2


class TaxAdminFactory(UserFactory):

    user_type = 3


class TaxFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TaxCalc

    user = factory.SubFactory(TaxPayerFactory)
    baseIncome = factory.Faker("pyfloat", left_digits=5, right_digits=2, positive=True)
    allowance = factory.Faker("pyfloat", left_digits=5, right_digits=2, positive=True)
    taxable_prereq = factory.Faker(
        "pyfloat", left_digits=5, right_digits=2, positive=True
    )
    income_from_property = factory.Faker(
        "pyfloat", left_digits=5, right_digits=2, positive=True
    )
    st_cap_gain_immovable = factory.Faker(
        "pyfloat", left_digits=5, right_digits=2, positive=True
    )
    lt_cap_gain_immovable = factory.Faker(
        "pyfloat", left_digits=5, right_digits=2, positive=True
    )
    pan = factory.Faker("pystr", min_chars=12, max_chars=15)
