from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied,ValidationError,NotFound
from rest_framework.response import Response
from core_apps.common.renderers import GenericJSONRenderer
from core_apps.profiles.models import Profile
from .serializers import RatingSerializer
from .models import Rating

User = get_user_model()

class RatingCreateAPIView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    renderer_classes = [GenericJSONRenderer]
    object_label = "Rating"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        rated_user_username = serializer.validated_data.get("rated_user_username")
        try:
            rated_user = User.objects.get(username=rated_user_username)
        except User.DoesNotExist:
            raise NotFound(f"User with username '{rated_user_username}' does not exist.")

        rating_user = request.user

        # Self-rating is never allowed
        if rating_user == rated_user:
            raise PermissionDenied("You cannot rate yourself.")

        # Both users must have a profile
        try:
            rating_occupation = rating_user.profile.occupation
            rated_occupation = rated_user.profile.occupation
        except Profile.DoesNotExist:
            raise ValidationError("Both users must have a valid occupation.")

        allowed_technicians = {
            Profile.Occupation.CARPENTER,
            Profile.Occupation.ELECTRICIAN,
            Profile.Occupation.HVAC,
            Profile.Occupation.MASON,
            Profile.Occupation.PAINTER,
            Profile.Occupation.PLUMBER,
            Profile.Occupation.ROOFER,
        }

        is_tenant = rating_occupation == Profile.Occupation.TENANT
        target_is_technician = rated_occupation in allowed_technicians

        if is_tenant and not target_is_technician:
            raise PermissionDenied("Tenants can only rate technicians.")

        if not is_tenant:
            raise PermissionDenied("Only tenants can submit ratings.")

        # Prevent duplicate ratings
        if Rating.objects.filter(rated_user=rated_user, rating_user=rating_user).exists():
            raise ValidationError("You have already rated this user.")

        rating = serializer.save(rating_user=rating_user, rated_user=rated_user)
        return Response(
            self.get_serializer(rating).data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(self.get_serializer(rating).data),
        )
