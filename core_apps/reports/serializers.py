import logging

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from .emails import send_deactivation_email, send_warning_email
from .models import Report

logger = logging.getLogger(__name__)
User = get_user_model()

class ReportSerializer(serializers.ModelSerializer):
    reported_user_username = serializers.CharField(write_only=True)

    class Meta:
        model = Report
        fields = ["id","title","description","reported_user_username","created_at"]

    def validate_reported_user_username(self, value:str)->str:
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError("The provided username does not exist")
        return value    
        
    def create(self, validated_data:dict)->Report:
        username = validated_data.pop("reported_user_username")
        try:
            reported_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("The tenant with that username does not exist.")
        report = Report.objects.create(reported_user=reported_user, **validated_data)
        return report

