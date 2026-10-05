from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
import logging
from core_apps.common.models import ContentView

logger = logging.getLogger(__name__)

class IssueViewMixin:
    def record_issue_view(self, issue) -> None:
        try:
            content_type = ContentType.objects.get_for_model(issue)
            viewer_ip = self.get_client_ip()
            user = self.request.user

            obj, created = ContentView.objects.get_or_create(
                content_type=content_type,
                object_id=issue.id,
                user=user,
                viewer_ip=viewer_ip,
                defaults={"last_viewed": timezone.now()},
            )
        except Exception as e:

            logger.info(f"Failed to record view for Issue ID: {issue.id}: {e}")

    def get_client_ip(self) -> str:
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = self.request.META.get("REMOTE_ADDR")
        return ip
