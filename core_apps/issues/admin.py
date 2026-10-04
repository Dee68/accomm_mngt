from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from core_apps.common.models import ContentView
from .models import Issue

User = get_user_model()


class AssignmentStatusFilter(admin.SimpleListFilter):
    title = "assignment status"
    parameter_name = "assigned"

    def lookups(self, request, model_admin):
        return (
            ("unassigned", "Unassigned"),
            ("assigned", "Assigned"),
        )

    def queryset(self, request, queryset):
        if self.value() == "unassigned":
            return queryset.filter(assigned_to__isnull=True)
        if self.value() == "assigned":
            return queryset.filter(assigned_to__isnull=False)
        return queryset


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "apartment",
        "reported_by",
        "assigned_to",
        "status",
        "priority",
        "get_total_views",
    ]
    list_display_links = ["id", "apartment"]
    list_filter = ["status", "priority", AssignmentStatusFilter]
    search_fields = ["apartment__unit_number", "reported_by__first_name"]
    ordering = ["-created_at"]
    autocomplete_fields = ["apartment", "reported_by"]

    actions = ["mark_in_progress", "mark_resolved"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "assigned_to":
            kwargs["queryset"] = User.objects.filter(
                profile__occupation__in=[
                    "mason", "plumber", "painter", "roofer",
                    "electrician", "carpenter", "hvac",
                ]
            )
            is_staff=False,
            is_superuser=False,
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == "assigned_to":
            formfield.label_from_instance = lambda obj: (
                f"{obj.email} — {obj.profile.get_occupation_display()}"
            )

        return formfield

    def get_total_views(self, obj) -> int:
        content_type = ContentType.objects.get_for_model(obj)
        return ContentView.objects.filter(
            content_type=content_type,
            object_id=obj.id,
        ).count()

    get_total_views.short_description = "Total Views"

    @admin.action(description="Mark selected issues as in progress")
    def mark_in_progress(self, request, queryset):
        for issue in queryset:
            issue.status = Issue.IssueStatus.IN_PROGRESS
            issue.save()
        self.message_user(
            request,
            f"{queryset.count()} issue(s) marked as in progress.",
        )

    @admin.action(description="Mark selected issues as resolved")
    def mark_resolved(self, request, queryset):
        count = 0
        for issue in queryset:
            issue.status = Issue.IssueStatus.RESOLVED
            issue.resolved_on = timezone.now().date()
            issue.save()
            count += 1
        self.message_user(
            request,
            f"{count} issue(s) marked as resolved.",
        )