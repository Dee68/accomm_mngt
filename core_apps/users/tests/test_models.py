import pytest
from django.db import IntegrityError
from django.core.exceptions import ValidationError
import uuid

from core_apps.users.models import User


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(
        email="john@example.com",
        username="john",
        first_name="John",
        last_name="Doe",
        password="TestPassword123!",
    )

    assert user.email == "john@example.com"
    assert user.username == "john"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.pk is not None
    assert user.id is not None


@pytest.mark.django_db
def test_email_is_unique():
    User.objects.create_user(
        email="john@example.com",
        username="john",
        first_name="John",
        last_name="Doe",
        password="TestPassword123!",
    )

    with pytest.raises(IntegrityError):
        User.objects.create_user(
            email="john@example.com",
            username="john2",
            first_name="Jane",
            last_name="Doe",
            password="TestPassword123!",
        )


@pytest.mark.django_db
def test_username_is_unique():
    User.objects.create_user(
        email="john@example.com",
        username="john",
        first_name="John",
        last_name="Doe",
        password="TestPassword123!",
    )

    with pytest.raises(IntegrityError):
        User.objects.create_user(
            email="jane@example.com",
            username="john",
            first_name="Jane",
            last_name="Doe",
            password="TestPassword123!",
        )


@pytest.mark.django_db
def test_password_is_hashed():
    user = User.objects.create_user(
        email="john@example.com",
        username="john",
        first_name="John",
        last_name="Doe",
        password="TestPassword123!",
    )

    assert user.password != "TestPassword123!"
    assert user.check_password("TestPassword123!")


@pytest.mark.django_db
def test_get_full_name():
    user = User.objects.create_user(
        email="john@example.com",
        username="john",
        first_name="John",
        last_name="Doe",
        password="TestPassword123!",
    )

    assert user.get_full_name == "John Doe"


@pytest.mark.django_db
def test_get_full_name_with_only_first_name():
    user = User.objects.create_user(
        email="john@example.com",
        username="john",
        first_name="John",
        last_name="",
        password="TestPassword123!",
    )

    assert user.get_full_name == "John"


@pytest.mark.django_db
def test_get_full_name_with_only_last_name():
    user = User.objects.create_user(
        email="john@example.com",
        username="john",
        first_name="",
        last_name="Doe",
        password="TestPassword123!",
    )

    assert user.get_full_name == "Doe"


@pytest.mark.django_db
def test_id_is_uuid():
    user = User.objects.create_user(
        email="john@example.com",
        username="john",
        first_name="John",
        last_name="Doe",
        password="TestPassword123!",
    )

    assert isinstance(user.id, uuid.UUID)


@pytest.mark.django_db
def test_users_have_unique_uuid_ids():
    user1 = User.objects.create_user(
        email="john@example.com",
        username="john",
        first_name="John",
        last_name="Doe",
        password="TestPassword123!",
    )

    user2 = User.objects.create_user(
        email="jane@example.com",
        username="jane",
        first_name="Jane",
        last_name="Doe",
        password="TestPassword123!",
    )

    assert user1.id != user2.id


@pytest.mark.django_db
def test_pkid_is_primary_key():
    user = User.objects.create_user(
        email="john@example.com",
        username="john",
        first_name="John",
        last_name="Doe",
        password="TestPassword123!",
    )

    assert user.pk == user.pkid
    assert user.pkid is not None


@pytest.mark.django_db
def test_id_is_not_primary_key():
    field = User._meta.get_field("id")
    assert field.primary_key is False


@pytest.mark.django_db
@pytest.mark.parametrize(
    "username",
    [
        "john",
        "john.doe",
        "john_doe",
        "john-doe",
        "john+doe",
        "john@doe",
        "john123",
    ],
)
def test_valid_username(username):
    user = User(
        email="john@example.com",
        username=username,
        first_name="John",
        last_name="Doe",
        password="TestPassword123!",
    )

    user.full_clean()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "username",
    [
        "john doe",
        "john!",
        "john#",
        "john$",
        "john%",
        "john&",
    ],
)
def test_invalid_username(username):
    user = User(
        email="john@example.com",
        username=username,
        first_name="John",
        last_name="Doe",
        password="TestPassword123!",
    )

    with pytest.raises(ValidationError):
        user.full_clean()