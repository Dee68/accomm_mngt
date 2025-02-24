"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.http import JsonResponse

Schema_view = get_schema_view(
    openapi.Info(
        title="Accommodation Management API",
        default_version="v1",
        description="An Accommodation management API for accommodation centre",
        contact=openapi.Contact(email="admin@golden-ventures.com"),
        license=openapi.License(name="MIT License")
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

def health_check(request):
    return JsonResponse({"status": "healthy"})

urlpatterns = [
    path("redoc/", Schema_view.with_ui("redoc",cache_timeout=0)),
    path("health/",health_check),
    path(settings.ADMIN_URL, admin.site.urls),
]

admin.site.site_header = "Accommodation Centre Admin"
admin.site.site_title = "Accommodation Admin Portal"
admin.site.index_title = "Welcome to Accommodation Admin Portal"
