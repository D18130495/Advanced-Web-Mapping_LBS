from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from django_restful_api import rest_views, overpass_view


router = routers.DefaultRouter()
router.register(r'users', rest_views.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api-auth/", include('rest_framework.urls', namespace='rest_framework')),
    path("api/login/", rest_views.Login.as_view(), name="login"),
    path("api/logout/", rest_views.Logout.as_view(), name="logout"),
    path("api/signup/", rest_views.RegisterUser.as_view(), name="signup"),
    path("api/changePassword/", rest_views.ChangePassword.as_view(), name="changePassword"),
    path("api/getCurrentUserInfo/", rest_views.GetCurrentUserInfo.as_view(), name="getCurrentUserInfo"),
    path("api/updateProfile/", rest_views.UpdateProfile.as_view(), name="updateProfile"),
    path("api/updateLocation/", rest_views.UpdateLocation.as_view(), name="updateLocation"),
    path("api/queryOverpass/", overpass_view.QueryOverpass.as_view(), name="queryOverpass")
]
