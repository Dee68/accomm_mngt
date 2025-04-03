from rest_framework import generics
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from .serializers import ReportSerializer
from .models import Report
from core_apps.common.renderers import GenericJSONRenderer


class StandardResultSetPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = "page_size"
    max_page_size = 100

class CreateReportAPIView(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    renderer_classes = [GenericJSONRenderer]
    object_label = "Report"

    def perform_create(self, serializer:serializers.Serializer)->None:
        serializer.save(reported_by=self.request.user)

class ReportListAPIView(generics.ListAPIView):
    serializer_class = ReportSerializer
    renderer_classes = [GenericJSONRenderer]
    object_label = "Reports"

    def get_queryset(self)->Report:
        user = self.request.user
        return Report.objects.filter(reported_by=user)

