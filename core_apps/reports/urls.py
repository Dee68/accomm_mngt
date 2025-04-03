from django.urls import path
from .views import CreateReportAPIView, ReportListAPIView


urlpatterns = [
    path("create/", CreateReportAPIView.as_view(), name="create-report"),
    path("me/", ReportListAPIView.as_view(), name="my-reports")
]
