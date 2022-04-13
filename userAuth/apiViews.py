from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.serializers import ModelSerializer
from . import models
from rest_framework.views import Response
from rest_framework.decorators import action

# ps: i could have used custom created permission classes, but that would have been an overkill, so i stuck with checking the user's clearance.


class TaxRateViewSet(ReadOnlyModelViewSet):
    class TaxRateSerializer(ModelSerializer):
        class Meta:
            model = models.TaxRates
            exclude = ()

    serializer_class = TaxRateSerializer
    queryset = models.TaxRates.objects.all()


class UserViewSet(ModelViewSet):
    class UserSerializer(ModelSerializer):
        class Meta:
            model = models.User
            fields = [
                "id",
                "username",
                "email",
                "first_name",
                "last_name",
                "is_staff",
                "is_superuser",
                "is_active",
                "date_joined",
                "user_type",
                "state",
            ]

    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.user_type not in (2, 3):
            return models.User.objects.filter(pk=self.request.user.pk)
        else:
            return models.User.objects.all()


class TaxCalcViewSet(ModelViewSet):
    class TaxCalcSerializer(ModelSerializer):
        class Meta:
            model = models.TaxCalc
            fields = [
                "id",
                "user",
                "baseIncome",
                "allowance",
                "taxable_prereq",
                "income_from_property",
                "st_cap_gain_immovable",
                "lt_cap_gain_immovable",
                "total_taxable_income",
                "total_tax",
                "gst",
                "due_on",
                "paid",
                "updated_on",
                "state",
            ]

    serializer_class = TaxCalcSerializer

    def get_queryset(self):
        if self.request.user.user_type not in (2, 3):
            return models.TaxCalc.objects.filter(user=self.request.user)
        else:
            return models.TaxCalc.objects.all()

    def update(self, request, *args, **kwargs):
        if self.request.user.user_type != 2:
            return Response(
                {"detail": "You are not allowed to update this."}, status=403
            )
        try:
            return super(TaxCalcViewSet, self).update(request, *args, **kwargs)
        except models.TaxCalc.AlreadyPaidException:
            return Response(
                {"detail": "This tax calculation has already been paid."},
                status=403,
            )

    def partial_update(self, request, *args, **kwargs):
        if self.request.user.user_type != 2:
            return Response(
                {"detail": "You are not allowed to update this."}, status=403
            )
        try:
            return super().partial_update(request, *args, **kwargs)
        except models.TaxCalc.AlreadyPaidException:
            return Response(
                {"detail": "This tax calculation has already been paid."},
                status=403,
            )

    def create(self, request, *args, **kwargs):
        if self.request.user.user_type != 2:
            return Response(
                {"detail": "You are not allowed to create this."}, status=403
            )
        try:
            return super(TaxCalcViewSet, self).create(request, *args, **kwargs)
        except models.TaxCalc.AlreadyPaidException:
            return Response(
                {"detail": "This tax calculation has already been paid."},
                status=403,
            )

    def destroy(self, request, *args, **kwargs):
        if self.request.user.user_type != 2:
            return Response(
                {"detail": "You are not allowed to delete this."}, status=403
            )
        try:
            return super(TaxCalcViewSet, self).destroy(request, *args, **kwargs)
        except models.TaxCalc.AlreadyPaidException:
            return Response(
                {"detail": "This tax calculation has already been paid."},
                status=403,
            )

    @action(detail=True, methods=["post", "get"])
    def set_paid(self, request, pk=None):

        obj = self.get_queryset().get(pk=pk)

        if obj.user.pk == request.user.pk:
            if request.method == "POST":
                obj.setPaid()
            try:
                return Response({"paid": models.TaxCalc.objects.get(pk=pk).paid})
            except models.TaxCalc.AlreadyPaidException:
                return Response(
                    {"detail": "This tax calculation has already been paid."},
                    status=403,
                )
