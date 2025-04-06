from django.contrib import admin
from django.db.models import Avg
from .models import Rating

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ["rated_user","rating_user","comment","rating","get_average_rating"]
    search_fields = ["rated_user__username","rating_user__username"]
    list_filter = ["rating","created_at"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            average_rating = Avg("rated_user__received_ratings__rating")

        )
        return queryset
    
    def get_average_rating(self,obj):
        return round(obj.average_rating,2) if obj.average_rating is not None else None
    
    get_average_rating.short_description = "Average Rating"
    get_average_rating.admin_order_fields = "average_rating"
