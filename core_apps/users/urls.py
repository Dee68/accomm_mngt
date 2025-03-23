from django.urls import path,re_path
#from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (CustomProviderAuthView,
                    CustomTokenObtainPairView,CustomTokenRefreshView,LogoutAPIView)

urlpatterns = [
    re_path(r"^o/(?P<provider>\S+)/$", CustomProviderAuthView.as_view(), name="provider-auth"),
    #path("login/", TokenObtainPairView.as_view()),
    path("login/", CustomTokenObtainPairView.as_view()),
    path("refresh/", CustomTokenRefreshView.as_view()),
    path("logout/", LogoutAPIView.as_view()),
]
