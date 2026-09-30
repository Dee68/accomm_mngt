import pytest

from core_apps.users.models import User
from core_apps.profiles.models import Profile
from core_apps.users.serializers import (
    CreateUserSerializer,
    CustomUserSerializer,
)
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch


@pytest.mark.django_db
class TestCreateUserSerializer:

    def test_create_user_serializer_valid_data(self):
        data = {
            "username": "john",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "TestPassword123!",
        }

        serializer = CreateUserSerializer(data=data)

        assert serializer.is_valid(), serializer.errors

    def test_create_user_serializer_creates_user(self): 
        data = { "username": "john", 
                "email": "john@example.com", 
                "first_name": "John", 
                "last_name": "Doe", 
                "password": "TestPassword123!", 
                } 
        serializer = CreateUserSerializer(data=data) 
        assert serializer.is_valid(), serializer.errors 
        user = serializer.save() 
        assert User.objects.filter(email="john@example.com").exists() 
        assert user.username == "john" 
        assert user.first_name == "John" 
        assert user.last_name == "Doe" 
        assert user.check_password("TestPassword123!")

    
    def test_create_user_serializer_includes_email(self):
        data = {
            "username": "john",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "TestPassword123!",
        }

        serializer = CreateUserSerializer(data=data)

        assert serializer.is_valid(), serializer.errors

        assert "email" in serializer.validated_data

    
    def test_create_user_serializer_requires_email(self):
        data = {
            "username": "john",
            "first_name": "John",
            "last_name": "Doe",
            "password": "TestPassword123!",
        }

        serializer = CreateUserSerializer(data=data)

        assert not serializer.is_valid()
        assert "email" in serializer.errors

    
    def test_create_user_serializer_password_is_write_only(self):
        serializer = CreateUserSerializer()

        assert serializer.fields["password"].write_only is True

    
    @pytest.mark.django_db
    def test_create_user_serializer_rejects_duplicate_email(self):
        User.objects.create_user(
            username="existing",
            email="existing@example.com",
            password="TestPassword123!",
            first_name="Existing",
            last_name="User",
        )

        data = {
            "username": "newuser",
            "email": "existing@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "TestPassword123!",
        }

        serializer = CreateUserSerializer(data=data)

        assert not serializer.is_valid()
        assert "email" in serializer.errors




@pytest.mark.django_db
class TestCustomUserSerializer:

    def test_custom_user_serializer_basic_fields(self):
        user = User.objects.create_user(
            username="john",
            email="john@example.com",
            password="TestPassword123!",
            first_name="John",
            last_name="Doe",
        )

        serializer = CustomUserSerializer(user)

        assert serializer.data["id"] == str(user.id)
        assert serializer.data["email"] == "john@example.com"
        assert serializer.data["username"] == "john"
        assert serializer.data["first_name"] == "John"
        assert serializer.data["last_name"] == "Doe"
        assert serializer.data["full_name"] == "John Doe"

    
    def test_custom_user_serializer_read_only_fields(self):
        serializer = CustomUserSerializer()

        assert serializer.fields["id"].read_only is True
        assert serializer.fields["email"].read_only is True
        assert serializer.fields["date_joined"].read_only is True

    
    
    def test_custom_user_serializer_profile_fields(self):
        user = User.objects.create_user(
            username="john",
            email="john@example.com",
            password="TestPassword123!",
            first_name="John",
            last_name="Doe",
        )

        profile = user.profile
        profile.gender = Profile.Gender.MALE
        profile.occupation = Profile.Occupation.TENANT
        profile.phone_number = "+353877800112"
        profile.country_field = "IE"
        profile.city_of_origin = "Dublin"
        profile.reputation = 100
        profile.save()

        serializer = CustomUserSerializer(user)

        assert serializer.data["gender"] == "male"
        assert serializer.data["occupation"] == "tenant"
        assert serializer.data["phone_number"] == "+353877800112"
        assert serializer.data["country"] == "IE"
        assert serializer.data["city"] == "Dublin"
        assert serializer.data["reputation"] == 100
        assert serializer.data["slug"] == profile.slug

    
    def test_custom_user_serializer_avatar_without_avatar(self):
        user = User.objects.create_user(
            username="john",
            email="john@example.com",
            password="TestPassword123!",
            first_name="John",
            last_name="Doe",
        )

        serializer = CustomUserSerializer(user)

        assert "avatar" not in serializer.data

    @pytest.mark.django_db
    def test_custom_user_serializer_avatar_with_avatar(self):
        user = User.objects.create_user(
            username="john",
            email="john@example.com",
            password="StrongPassword123!",
            first_name="John",
            last_name="Doe",
        )

        profile = user.profile

        avatar = SimpleUploadedFile(
            "john-doe.jpg",
            b"fake-image-content",
            content_type="image/jpeg",
        )

        with patch("cloudinary.uploader.upload") as mock_upload:
            mock_upload.return_value = {
                "public_id": "avatars/john-doe",
                "version": 123456,
                "format": "jpg",
                "type": "upload",
                "resource_type": "image",
            }

            profile.avatar = avatar
            profile.save()

        serializer = CustomUserSerializer(user)

        #print("avatar:", profile.avatar)
        #print("avatar url:", profile.avatar.url)
        #print("serializer data:", serializer.data)

        assert "avatar" in serializer.data
        assert serializer.data["avatar"]





