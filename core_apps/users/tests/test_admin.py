from django.contrib import admin
from django.contrib.auth import get_user_model

from core_apps.users.admin import UserAdmin

User = get_user_model()


class TestUserAdmin:

    def test_user_admin_is_registered(self):
        assert admin.site.is_registered(User)

    def test_user_admin_uses_custom_admin_class(self):
        registered_admin = admin.site._registry[User]

        assert isinstance(registered_admin, UserAdmin)

    def test_user_admin_list_display(self):
        assert UserAdmin.list_display == [
            "pkid",
            "id",
            "email",
            "first_name",
            "last_name",
            "username",
            "is_superuser",
        ]

    def test_user_admin_search_fields(self):
        assert UserAdmin.search_fields == [
            "email",
            "first_name",
            "last_name",
        ]

    def test_user_admin_ordering(self):
        assert UserAdmin.ordering == ["pkid"]
        

    def test_user_admin_fieldsets(self):
        assert UserAdmin.fieldsets == (
            (
                "Login Credentials",
                {"fields": ("email", "password")},
            ),
            (
                "Personal Info",
                {"fields": ("first_name", "last_name", "username")},
            ),
            (
                "Permissions and Groups",
                {
                    "fields": (
                        "is_active",
                        "is_staff",
                        "is_superuser",
                        "groups",
                        "user_permissions",
                    )
                },
            ),
            (
                "Important Dates",
                {"fields": ("last_login", "date_joined")},
            ),
        )

    def test_user_admin_add_fieldsets(self):
        assert UserAdmin.add_fieldsets == (
            (
                None,
                {
                    "classes": ("wide",),
                    "fields": (
                        "username",
                        "email",
                        "first_name",
                        "last_name",
                        "password1",
                        "password2",
                    ),
                },
            ),
        )