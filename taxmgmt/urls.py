"""taxmgmt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from userAuth import apiViews, webViews
from rest_framework import routers
from rest_framework.authtoken import views as tokenViews

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Tax Management API",
        default_version="v0",
        description="Api description and schema",
        terms_of_service="",
        contact=openapi.Contact(email="grimmgagan@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


router = routers.DefaultRouter()

router.register("taxrates", apiViews.TaxRateViewSet)
router.register("users", apiViews.UserViewSet, "users")
router.register("taxcalc", apiViews.TaxCalcViewSet, "taxcalc")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("login/", webViews.LoginView.as_view(), name="login"),
    path("logout/", webViews.LogoutView.as_view(), name="logout"),
    path("createUser/", webViews.CreateUserView.as_view(), name="createUser"),
    path("createTax/<int:pk>", webViews.CreateTaxView.as_view(), name="createTax"),
    path("viewUsers/", webViews.ViewUsersView.as_view(), name="viewUsers"),
    path("", webViews.IndexView.as_view(), name="index"),
    path("api/auth/", tokenViews.obtain_auth_token),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
