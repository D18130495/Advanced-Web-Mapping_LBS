"""Advanced_Web_Mapping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from awm2023 import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("signup.urls")),
    path("logout/", auth_views.LogoutView.as_view(template_name="registration/logout.html"), name="logout"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/changePasswordDone.html'), name="changePasswordDone"),
    path("", include("django.contrib.auth.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("login/", TemplateView.as_view(template_name="registration/login.html"), name="login"),
    path("update-profile/", views.update_profile, name="updateProfile"),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='registration/changePassword.html'),
         name="changePassword"),
    path("map/", TemplateView.as_view(template_name="map.html"), name="map"),
    path("updatedb/", views.update_location, name="update_db"),
]
