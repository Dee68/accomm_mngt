from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


def health_check(request):
    return JsonResponse({"status": "healthy"})


urlpatterns = [
    path("health/", health_check),
    path(settings.ADMIN_URL, admin.site.urls),

    # API docs (DRF Spectacular)
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # API routes
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("core_apps.users.urls")),
    path("api/v1/profiles/", include("core_apps.profiles.urls")),
    path("api/v1/apartments/", include("core_apps.apartments.urls")),
    path("api/v1/issues/", include("core_apps.issues.urls")),
    path("api/v1/reports/", include("core_apps.reports.urls")),
    path("api/v1/ratings/", include("core_apps.ratings.urls")),
    path("api/v1/posts/", include("core_apps.posts.urls")),
]

admin.site.site_header = "Accommodation Center Admin"
admin.site.site_title = "Accommodation Admin Portal"
admin.site.index_title = "Welcome to Accommodation Admin Portal"