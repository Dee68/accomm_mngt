from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied,ValidationError,NotFound
from rest_framework.response import Response
from core_apps.common.renderers import GenericJSONRenderer
from core_apps.profiles.models import Profile
from .serializers import RatingSerializer

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
            raise NotFound(f"User with username '{rated_user_username} does not exist.")
        rating_user = request.user
        if rating_user == rated_user:
            raise PermissionDenied(f"You cannot rate yourself.")
        
        try:
            rating_user_occupation = rating_user.profile.occupation
            rated_user_occupation = rated_user.profile.occupation
        except Profile.DoesNotExist:
            raise ValidationError("Both users must have a valid occupation.")
        
        if(rating_user_occupation==Profile.Occupation.TENANT and rated_user_occupation==Profile.Occupation.TENANT):
            raise PermissionDenied("A tenant can not review another tenant.")
        allowed_occupations = [
            Profile.Occupation.CARPENTER,
            Profile.Occupation.ELECTRICIAN,
            Profile.Occupation.HVAC,
            Profile.Occupation.MASON,
            Profile.Occupation.PAINTER,
            Profile.Occupation.PLUMBER,
            Profile.Occupation.ROOFER
        ]

        if(rating_user_occupation==Profile.Occupation.TENANT and rated_user_occupation not in allowed_occupations):
            raise PermissionDenied("A tenant can only review technicians but not other tenants.")
        if(rating_user_occupation != Profile.Occupation.TENANT and rating_user == rated_user):
            raise PermissionDenied("A technician can not review themselves.")
        
        if(rating_user_occupation != Profile.Occupation.TENANT and rated_user_occupation != Profile.Occupation.TENANT):
            raise PermissionDenied("A technician can not review another technician.")
        
        rating = serializer.save(rating_user=rating_user,rated_user=rated_user)
        serializer = self.get_serializer(rating)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data,status=status.HTTP_201_CREATED,headers=headers)
