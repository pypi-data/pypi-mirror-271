from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from mozilla_django_oidc_db.views import (
    AdminLoginFailure,
    OIDCAuthenticationRequestView,
)

urlpatterns = [
    path("admin/login/failure/", AdminLoginFailure.as_view(), name="admin-oidc-error"),
    path("admin/", admin.site.urls),
    path("login", OIDCAuthenticationRequestView.as_view(), name="login"),
    path("oidc/", include("mozilla_django_oidc.urls")),
] + staticfiles_urlpatterns()
