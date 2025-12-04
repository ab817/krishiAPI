from django.contrib import admin
from .models import VetRequest, AboutUs, UserProfile

@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'mobile_number')
    search_fields = ('user__username', 'mobile_number')

@admin.register(VetRequest)
class VetRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'farmer', 'animal_type', 'status', 'location', 'created_at')
    list_filter = ('status', 'animal_type', 'created_at')
    search_fields = ('farmer__username', 'animal_type', 'location')
    ordering = ('-created_at',)


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'updated_at')
    search_fields = ('title',)
    ordering = ('-updated_at',)
