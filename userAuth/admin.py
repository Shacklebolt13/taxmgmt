from django.contrib import admin
from . import models

from django.contrib.auth.admin import UserAdmin


@admin.register(models.User)
class UserAdminAdvanced(UserAdmin):
    UserAdmin.list_display += ("user_type", "state")
    UserAdmin.list_filter += ("user_type", "state")
    UserAdmin.search_fields += ("user_type", "state")

    UserAdmin.fieldsets += (("Special Details", {"fields": ("user_type", "state")}),)
    UserAdmin.add_fieldsets += (
        ("Special Details", {"fields": ("user_type", "state")}),
    )

    def save_model(self, request, obj, form, change) -> None:

        obj.save(clearance=request.user.user_type)


@admin.register(models.TaxCalc)
class TaxCalcAdmin(admin.ModelAdmin):
    list_display = ("user", "finalAmt", "paid")

    def paid(self, obj):
        return "Paid" if obj.paid else "Not Paid"


@admin.register(models.TaxRates)
class TaxRatesAdmin(admin.ModelAdmin):
    list_display = ("name", "Gst")

    def Gst(self, obj):
        return f"{obj.rate:2.0f}%"
