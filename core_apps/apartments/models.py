from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from core_apps.common.models import TimeStampedModel

User = get_user_model()

class Apartment(TimeStampedModel):
    unit_number = models.CharField(max_length=10,verbose_name=_("Unit Number"),unique=True)
    building = models.CharField(max_length=50,verbose_name=_("Building"))
    floor = models.PositiveIntegerField(verbose_name=_("Floor"))
    tenant = models.OneToOneField(User,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name="apartment",
                                blank=True,verbose_name=_("Tenant"))
    

    def __str__(self):
        return f"Unit: {self.unit_number} - Building: {self.building} - Floor: {self.floor}"
