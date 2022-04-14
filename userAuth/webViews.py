from django.http import HttpRequest
from django.views import View
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout, authenticate, login
from . import forms, models
from django.db.models import Q, Sum


# ps: i could have used custom created permission classes, but that would have been an overkill, so i stuck with checking the user's clearance.


class LoginView(View):
    def get(self, request: HttpRequest):
        return render(request, "userAuth/login.html")

    def post(self, request: HttpRequest):
        if not request.user.is_anonymous:
            return redirect("index")

        username = request.POST.get("username", None)
        password = request.POST.get("password", None)

        dictV = {}
        if username is None or password is None:
            dictV["error"] = "Both Fields Are Mandatory"
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                dictV["error"] = "Check Your UserName and Password"
            else:
                login(request, user)

                return redirect(request.GET.get("next", "index"))

        return render(request, "userAuth/login.html", status=400, context=dictV)


@method_decorator(login_required, name="get")
class LogoutView(View):
    def get(self, request: HttpRequest):
        logout(request)
        return redirect("index")


@method_decorator(login_required, name="get")
@method_decorator(login_required, name="post")
class CreateUserView(View):
    def get(self, request: HttpRequest):
        if request.user.user_type < 2:
            return redirect("index")
        dictV = {"userform": forms.createUserForm}
        return render(request, "userAuth/createUser.html", dictV)

    def post(self, request: HttpRequest):
        if request.user.user_type < 2:
            return redirect("index")

        pwd = request.POST.get("password", None)
        if pwd is None:
            return render(
                request,
                "userAuth/createUser.html",
                status=400,
                context={"error": "Password is Mandatory"},
            )
        userform = forms.createUserForm(request.POST)
        if userform.is_valid():
            user = userform.save()
            user.set_password(pwd)
            user.save()
            return redirect("index")
        else:
            dictV = {"userform": userform}
            return render(request, "userAuth/createUser.html", dictV, status=400)


@method_decorator(login_required, name="get")
class ViewUsersView(View):
    def get(self, request: HttpRequest):
        dictV = {
            "users": models.User.objects.all()
            .annotate(
                total_due=Sum(
                    "taxcalc__finalAmt", filter=Q(taxcalc__paid_on__isnull=True)
                )
            )
            .filter(user_type__lte=request.user.user_type)
        }
        return render(request, "userAuth/viewUsers.html", dictV)


@method_decorator(login_required, name="get")
class IndexView(View):
    def get(self, request: HttpRequest):
        taxes = (
            request.user.taxcalc_set.all()
            if request.user.user_type == 1
            else models.TaxCalc.objects.all()
        )
        dictV = {"taxes": taxes}
        return render(request, "userAuth/index.html", dictV)

    def post(self, request: HttpRequest):
        pk = request.POST.get("pay", None)
        tax = models.TaxCalc.objects.get(pk=pk)
        if tax.user.pk == request.user.pk:
            tax.setPaid()
            return redirect("index")
        taxes = (
            request.user.taxcalc_set.all()
            if request.user.user_type == 1
            else models.TaxCalc.objects.all()
        )
        dictV = {"taxes": taxes, "error": "You are not authorized to pay this tax"}
        return render(request, "userAuth/index.html", dictV)


@method_decorator(login_required, name="get")
class CreateTaxView(View):
    def get(self, request: HttpRequest, pk):
        if request.user.user_type != 2:
            return redirect("index")
        dictV = {"taxform": forms.createTaxForm}
        return render(request, "userAuth/createTax.html", dictV)

    def post(self, request: HttpRequest, pk):
        dictV = {"taxform": forms.createTaxForm}
        if request.user.user_type != 2:
            return redirect("index")
        data = request.POST.copy()
        taxform = forms.createTaxForm(request.POST)
        if taxform.is_valid():
            tax = taxform.save(commit=False)
            tax.user = models.User.objects.get(pk=pk)
            tax.save()
            return redirect("index")
        else:
            dictV["error"] = taxform.errors
            return render(request, "userAuth/createTax.html", dictV, status=400)
