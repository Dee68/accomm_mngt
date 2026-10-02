from rest_framework import serializers
from .models import Apartment

class ApartmentSerializer(serializers.ModelSerializer):
    tenant = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Apartment
        exclude = ["pkid","updated_at"]

    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user if request else None

        if user:
            queryset = Apartment.objects.filter(tenant=user)

            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)

            if queryset.exists():
                raise serializers.ValidationError({
                    "tenant": "This user is already assigned to an apartment."
                })

        return attrs