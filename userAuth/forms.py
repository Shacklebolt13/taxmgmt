from django.forms import ModelForm
from . import models


class createUserForm(ModelForm):
    class Meta:
        model = models.User
        fields = ["username", "user_type", "state"]
