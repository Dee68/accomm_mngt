import logging

from django.contrib.auth import get_user_model
#from django.utils import timezone
from rest_framework import serializers
#from .emails import send_deactivation_email, send_warning_email
from .models import Report

logger = logging.getLogger(__name__)
User = get_user_model()

class ReportSerializer(serializers.ModelSerializer):
    reported_user_username = serializers.CharField(write_only=True)

    class Meta:
        model = Report
        fields = ["id","title","description","reported_user_username","created_at"]

    def validate_reported_user_username(self, value):
        # Strip white spaces and leading @ if present
        cleaned = value.strip().lstrip("@")
        user = (
        User.objects.filter(username__iexact=cleaned).first()
        or User.objects.filter(email__iexact=cleaned).first()
        )

        if not user:
            raise serializers.ValidationError(
                "Provided username does not exist."
            )

        self.reported_user = user
        return cleaned  
        
    def create(self, validated_data)->Report:
        validated_data.pop("reported_user_username")
        return Report.objects.create(
            reported_user=self.reported_user,
            **validated_data,
        )

