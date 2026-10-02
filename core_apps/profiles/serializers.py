from django_countries.fields import CountryField
from rest_framework import serializers

from .models import Profile
from core_apps.apartments.models import Apartment
from core_apps.apartments.serializers import ApartmentSerializer

class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")
    full_name = serializers.ReadOnlyField(source="user.get_full_name")
    username = serializers.CharField(source="user.username")
    country_field = CountryField()
    avatar = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(source="user.date_joined",read_only=True)
    apartment = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["id",
                  "slug",
                  "first_name",
                  "last_name",
                  "full_name",
                  "username",
                  "gender",
                  "country_field",
                  "city_of_origin",
                  "bio",
                  "occupation",
                  "reputation",
                  "date_joined",
                  "avatar",
                  "apartment",
                  "average_rating",
                  "reviews"]
        
    def get_avatar(self,obj:Profile)->str | None:
        try:
            return obj.avatar.url
        except AttributeError:
            return None
        
    def get_average_rating(self,obj:Profile):
        return obj.get_average_rating()

    def get_apartment(self, obj: Profile):
        try:
            apartment = obj.user.apartment
        except Apartment.DoesNotExist:
            return None

        return ApartmentSerializer(apartment).data
        
    def get_reviews(self, obj):
        ratings = obj.user.received_ratings.select_related("rating_user").order_by("-created_at")
        return [
            {
                "rating": r.rating,
                "comment": r.comment,
                "rated_by": r.rating_user.get_full_name,
                "created_at": r.created_at,
            }
            for r in ratings
        ]
        
        
class UpdateProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    full_name = serializers.SerializerMethodField()
    username = serializers.CharField(source="user.username")
    #country_of_origin = CountryField()

    class Meta:
        model = Profile
        fields = [
                  "first_name",
                  "last_name",
                  "full_name",
                  "username",
                  "gender",
                  "country_field",
                  "city_of_origin",
                  "bio",
                  "occupation",
                  "phone_number"
                  ]
        
    def get_full_name(self, obj):
        """Fetches full name from the user model property"""
        if obj.user:
            return obj.user.get_full_name
        return None
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})

        for attr, value in user_data.items():
            setattr(instance.user, attr, value)

        instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance
        
class AvatarUploadSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()
    class Meta:
        model = Profile
        fields = ["avatar"]
    