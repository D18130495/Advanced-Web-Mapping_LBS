import rest_framework.authtoken.views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from pwa.views import service_worker, manifest, offline
from rest_framework import routers
from django_restful_api import views
from django_restful_api import rest_views


router = routers.DefaultRouter()
router.register(r'users', rest_views.UserViewSet)
# router.register(r'changePassword', rest_views.ChangePassword.as_view(), basename="changePassword")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api-auth/", include('rest_framework.urls', namespace='rest_framework')),
    path("api/changePassword/", rest_views.ChangePassword.as_view(), name="changePassword"),




    # path("api-token-auth/", rest_framework.authtoken.views.obtain_auth_token),
    #
    #
    #
    #
    path("api/login/", views.login, name="login"),
    path("api/logout/", views.logout, name="logout"),
    path("api/signup/", views.signup, name="signup"),
    path("api/getUserInfoByToken/", views.get_user_info_by_token, name="getUserInfoByToken"),
    path("api/updateProfile/", views.update_profile, name="updateProfile"),
    # path("api/changePassword/", views.change_password, name="changePassword"),
    # re_path(r'^serviceworker\.js$', service_worker, name='serviceworker'),
    # re_path(r'^manifest\.json$', manifest, name='manifest'),
    # re_path('^offline/$', offline, name='offline'),
]

# """Advanced_Web_Mapping_LBS URL Configuration
#
# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/4.1/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import include, path
# from django.views.generic.base import TemplateView
# from django.contrib.auth import views as auth_views
# from awm2023 import views
#
# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path('api-auth/', include('rest_framework.urls')),
#     path("", include("signup.urls")),
#     path("logout/", auth_views.LogoutView.as_view(template_name="registration/logout.html"), name="logout"),
#     path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
#         template_name='registration/changePasswordDone.html'), name="changePasswordDone"),
#     path("", include("django.contrib.auth.urls")),
#     path("", TemplateView.as_view(template_name="home.html"), name="home"),
#     path("login/", TemplateView.as_view(template_name="registration/login.html"), name="login"),
#     path("update-profile/", views.update_profile, name="updateProfile"),
#     path('change-password/', auth_views.PasswordChangeView.as_view(template_name='registration/changePassword.html'),
#          name="changePassword"),
#     path("map/", TemplateView.as_view(template_name="map.html"), name="map"),
#     path("updatedb/", views.update_location, name="update_db"),
# ]
