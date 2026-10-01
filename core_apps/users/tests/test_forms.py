
import pytest

from django.contrib.auth import get_user_model

from core_apps.users.forms import UserChangeForm, UserCreationForm


User = get_user_model()


def test_user_change_form_uses_custom_user_model():
    form = UserChangeForm()

    assert form._meta.model is User
    assert list(form.fields.keys()) == [
        "first_name",
        "last_name",
        "username",
        "email",
        "password",
    ]

@pytest.mark.django_db
def test_user_creation_form_rejects_duplicate_email():
    User.objects.create_user(
        username="existinguser",
        email="existing@example.com",
        password="TestPassword123!",
        first_name="Existing",
        last_name="User",
    )

    form = UserCreationForm(
        data={
            "first_name": "New",
            "last_name": "User",
            "username": "newuser",
            "email": "existing@example.com",
            "password1": "TestPassword123!",
            "password2": "TestPassword123!",
        }
    )

    assert not form.is_valid()
    assert "email" in form.errors
    assert form.errors["email"] == [
        " A user with that email already exists."
    ]

@pytest.mark.django_db
def test_user_creation_form_rejects_duplicate_username():
    User.objects.create_user(
        username="existinguser",
        email="existing@example.com",
        password="TestPassword123!",
        first_name="Existing",
        last_name="User",
    )

    form = UserCreationForm(
        data={
            "first_name": "New",
            "last_name": "User",
            "username": "existinguser",
            "email": "new@example.com",
            "password1": "TestPassword123!",
            "password2": "TestPassword123!",
        }
    )

    assert not form.is_valid()
    assert "username" in form.errors
    assert form.errors["username"] == [
        "A user with that username already exists."
    ]

@pytest.mark.django_db
def test_user_creation_form_rejects_mismatched_passwords():
    form = UserCreationForm(
        data={
            "first_name": "New",
            "last_name": "User",
            "username": "newuser",
            "email": "new@example.com",
            "password1": "TestPassword123!",
            "password2": "DifferentPassword123!",
        }
    )

    assert not form.is_valid()
    assert "password2" in form.errors
    assert form.errors["password2"] == [
        "Passwords do not match"
    ]

@pytest.mark.django_db
def test_user_creation_form_accepts_valid_data():
    form = UserCreationForm(
        data={
            "first_name": "New",
            "last_name": "User",
            "username": "newuser",
            "email": "new@example.com",
            "password1": "TestPassword123!",
            "password2": "TestPassword123!",
        }
    )

    assert form.is_valid()

    user = form.save()

    assert user.first_name == "New"
    assert user.last_name == "User"
    assert user.username == "newuser"
    assert user.email == "new@example.com"
    assert user.check_password("TestPassword123!")