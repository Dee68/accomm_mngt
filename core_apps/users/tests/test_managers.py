import pytest

from django.core.exceptions import ValidationError

from core_apps.users.models import User



@pytest.mark.django_db
class TestUserManager:

    def test_create_user(self):
        user = User.objects._create_user(
            username="john",
            email="john@example.com",
            password="TestPassword123!",
            first_name="John",
            last_name="Doe",
        )

        assert user is not None
        assert user.username == "john"
        assert user.email == "john@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.check_password("TestPassword123!")
        assert user.pkid is not None
        assert user.id is not None

    def test_create_user_requires_username(self):
        with pytest.raises(ValueError, match="A username must be provided"):
            User.objects._create_user(
                username="",
                email="john@example.com",
                password="TestPassword123!",
                first_name="John",
                last_name="Doe",
            )

    def test_create_user_requires_email(self):
        with pytest.raises(ValueError, match="An email address must be provided"):
            User.objects._create_user(
                username="john",
                email="",
                password="TestPassword123!",
                first_name="John",
                last_name="Doe",
            )

    def test_create_user_rejects_invalid_email(self):
        with pytest.raises(ValidationError, match="Enter a valid email address"):
            User.objects._create_user(
                username="john",
                email="not-an-email",
                password="TestPassword123!",
                first_name="John",
                last_name="Doe",
            )

    def test_create_user_normalizes_email(self):
        user = User.objects._create_user(
            username="john",
            email="John@EXAMPLE.COM",
            password="TestPassword123!",
            first_name="John",
            last_name="Doe",
        )

        assert user.email == "John@example.com"


    def test_create_user_without_password(self):
        user = User.objects._create_user(
            username="john",
            email="john@example.com",
            password=None,
            first_name="John",
            last_name="Doe",
        )

        assert user is not None
        assert user.username == "john"
        assert user.email == "john@example.com"
        assert user.has_usable_password() is False

    # public  method: create_user
    def test_manager_create_user(self):
        user = User.objects.create_user(
            username="jane",
            email="jane@example.com",
            password="TestPassword123!",
            first_name="Jane",
            last_name="Doe",
        )

        assert user.username == "jane"
        assert user.email == "jane@example.com"
        assert user.first_name == "Jane"
        assert user.last_name == "Doe"
        assert user.check_password("TestPassword123!")
        assert user.is_staff is False
        assert user.is_superuser is False

    #extra_fields.setdefault("is_staff", False)
    #extra_fields.setdefault("is_superuser", False)
    def test_create_user_respects_is_staff_value(self):
        user = User.objects.create_user(
            username="jane_staff",
            email="jane_staff@example.com",
            password="TestPassword123!",
            first_name="Jane",
            last_name="Staff",
            is_staff=True,
        )

        assert user.is_staff is True
        assert user.is_superuser is False

    def test_create_user_respects_is_superuser_value(self):
        user = User.objects.create_user(
            username="jane_super",
            email="jane_super@example.com",
            password="TestPassword123!",
            first_name="Jane",
            last_name="Super",
            is_superuser=True,
        )

        assert user.is_superuser is True
        assert user.is_staff is False

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="AdminPassword123!",
            first_name="Admin",
            last_name="User",
        )

        assert user.username == "admin"
        assert user.email == "admin@example.com"
        assert user.first_name == "Admin"
        assert user.last_name == "User"
        assert user.check_password("AdminPassword123!")
        assert user.is_staff is True
        assert user.is_superuser is True

    def test_create_superuser_requires_is_staff_true(self):
        with pytest.raises(ValueError, match="Superuser must have is_staff=True"):
            User.objects.create_superuser(
                username="admin_staff",
                email="admin_staff@example.com",
                password="AdminPassword123!",
                first_name="Admin",
                last_name="Staff",
                is_staff=False,
            )

    def test_create_superuser_requires_is_superuser_true(self):
        with pytest.raises(ValueError, match="Super user must have is_superuser=True"):
            User.objects.create_superuser(
                username="admin_super",
                email="admin_super@example.com",
                password="AdminPassword123!",
                first_name="Admin",
                last_name="Super",
                is_superuser=False,
            )