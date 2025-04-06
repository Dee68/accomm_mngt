from autoslug import AutoSlugField
from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Avg

from core_apps.common.models import TimeStampedModel

User = get_user_model()

def get_user_username(instance:"Profile")->str:
    return instance.user.username

class Profile(TimeStampedModel):
    class Gender(models.TextChoices):
        MALE = ("male", _("Male"))
        FEMALE = ("female", _("female"))

    class Occupation(models.TextChoices):
        MASON = ("mason", _("Mason"))
        PLUMBER = ("plumber", _("Plumber"))
        PAINTER = ("painter", _("Painter"))
        ROOFER = ("roofer", _("Roofer"))
        ELECTRICIAN = ("electrician", _("Electrician"))
        CARPENTER = ("carpenter", _("Carpenter"))
        HVAC = ("hvac", _("Hvac"))
        TENANT = ("tenant", _("Tenant"))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = CloudinaryField(verbose_name=_("Avatar"), blank=True, null=True)
    gender = models.CharField(max_length=10,verbose_name=_("Gender"), choices=Gender.choices, default=Gender.MALE)
    occupation = models.CharField(max_length=20,verbose_name=_("Occupation"),choices=Occupation.choices, default=Occupation.TENANT)
    bio = models.TextField(verbose_name=_("Bio"),blank=True,null=True)
    phone_number = PhoneNumberField(verbose_name=_("Phone Number"),max_length=13,default="+353877800112")
    country_field = CountryField(verbose_name=_("Country Field"), default="IE")
    city_of_origin = models.CharField(verbose_name=_("City Of Origin"),max_length=100,default="Dublin")
    report_count = models.IntegerField(verbose_name=_("Report Count"),default=0)
    reputation = models.IntegerField(verbose_name=_("Reputation"),default=100)
    slug = AutoSlugField(populate_from=get_user_username, unique=True)

    @property
    def is_banned(self)->bool:
        return self.report_count >= 5
    
    def update_reputation(self)->int:
        self.reputation = max(0,100 - self.report_count*20)

    def save(self, *args, **kwargs):
        self.update_reputation()
        super().save(*args,**kwargs)

    def get_average_rating(self):
        average = self.user.received_ratings.aggregate(Avg("rating"))["rating__avg"]
        return average if average is not None else 0.0
        


