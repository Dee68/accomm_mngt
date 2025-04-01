import logging

from django.http import Http404
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from rest_framework import generics,permissions,status
from rest_framework.exceptions import PermissionDenied,ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response

from core_apps.common.models import ContentView
from core_apps.common.renderers import GenericJSONRenderer
from core_apps.apartments.models import Apartment
from .models import Issue
from .emails import send_issue_confirmation_email, send_resolution_email
from .serializers import IssueSerializer, IssueStatusUpdateSerializer
from .mixins import IssueViewMixin

logger = logging.getLogger(__name__)

class IsStaffOrSuperUser(permissions.BasePermission):
    def __init__(self)->None:
        self.message = None

    def has_permission(self, request, view):
        is_authorized = (request.user and request.user.is_authenticated 
                         and (request.user.is_staff or request.user.is_superuser))
        if not is_authorized:
            self.message = (
                "Access to this information is restricted to staff and admin users only"
            )
        return is_authorized
    
class StandardResultSetPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = "page_size"
    max_page_size = 100
    

class IssueListAPIView(generics.ListAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    renderer_classes = [GenericJSONRenderer]
    permission_classes = [IsStaffOrSuperUser]
    object_label = "issues"
    pagination_class = StandardResultSetPagination

class AssignedIssueListView(generics.ListAPIView):
    serializer_class = IssueSerializer
    renderer_classes = [GenericJSONRenderer]
    object_label = "assigned_issues"
    pagination_class = StandardResultSetPagination

    def get_queryset(self):
        user = self.request.user
        return Issue.objects.filter(assigned_to=user)
    
class MyIssueListAPIView(generics.ListAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    renderer_classes = [GenericJSONRenderer]
    pagination_class = StandardResultSetPagination
    object_label = "my_issues"

    def get_queryset(self):
        user = self.request.user
        return Issue.objects.filter(reported_by=user)
    
class IssueCreateAPIView(generics.CreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    renderer_classes = [GenericJSONRenderer]
    object_label = "issue"

    def perform_create(self, serializer: IssueSerializer) -> None:
        apartment_id = self.kwargs.get("apartment_id")
        if not apartment_id:
            raise ValidationError({"apartment_id": ["Apartment ID is required"]})

        try:
            apartment = Apartment.objects.get(id=apartment_id, tenant=self.request.user)
        except Apartment.DoesNotExist:
            raise PermissionDenied("You do not have permission to raise an issue for this apartment.")

        issue = serializer.save(reported_by=self.request.user, apartment=apartment)

        logger.info(f"Issue created successfully: {issue.id} for user {self.request.user.email}")

        send_issue_confirmation_email(issue)  # This must be called

        logger.info("send_issue_confirmation_email() function was called.")


class IssueDetailAPIView(IssueViewMixin,generics.RetrieveAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    lookup_field = "id"
    renderer_classes = [GenericJSONRenderer]
    object_label = "issue"

    def get_object(self)->Issue:
        issue = super().get_object()
        user = self.request.user
        if not (user == issue.reported_by or user.is_staff or user == issue.assigned_to):
            raise PermissionDenied("You do not have permission to view this issue")
        self.record_issue_view(issue)
        return issue
    
    
class IssueUpdateAPIView(IssueViewMixin,generics.UpdateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueStatusUpdateSerializer
    lookup_field = "id"
    renderer_classes = [GenericJSONRenderer]
    object_label = "issues"

    def get_object(self)->Issue:
        issue = super().get_object()
        user = self.request.user
        if not (user.is_staff or user==issue.assigned_to):
            logger.warning(f"Unauthorized issue status update attempt by user {user.get_full_name} on issue {issue.title}"
                   )
            raise PermissionDenied("You do not have permission to update the issue.")
        self.record_issue_view(issue)
        return issue
    
class IssueDeleteAPIView(generics.DestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    lookup_field = "id"

    def get_object(self)->Issue:
        try:
            issue = super().get_object()

        except Http404:
            raise Http404("Issue not found") from None
        user = self.request.user
        if not (user==issue.reported_by or user.is_staff):
            logger.warning(f"Unauthorized delete attempt by user {user.get_full_name} on issue {issue.title}"
                           )
            raise PermissionDenied("You have no permission to delete this issue")

        return issue
    
    def delete(self, request, *args, **kwargs)->Response:
        super().delete(request,*args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)

