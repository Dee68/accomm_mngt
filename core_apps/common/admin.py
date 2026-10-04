from django.contrib import admin

from .models import ContentView


@admin.register(ContentView)
class ContentViewAdmin(admin.ModelAdmin):
    list_display = ["content_object", "user", "viewer_ip", "created_at"]
