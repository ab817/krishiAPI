from django.contrib import admin
from .models import VetRequest, AboutUs, UserProfile


# ---------------------------------
# User Profile Admin
# ---------------------------------
@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'mobile_number',
        'role',
    )
    list_filter = ('role',)
    search_fields = (
        'user__username',
        'user__email',
        'mobile_number',
    )
    ordering = ('user__username',)


# ---------------------------------
# Vet Request Admin
# ---------------------------------
@admin.register(VetRequest)
class VetRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'farmer',
        'animal_type',
        'status',
        'location',
        'created_at',
    )
    list_filter = (
        'status',
        'animal_type',
        'created_at',
    )
    search_fields = (
        'farmer__username',
        'animal_type',
        'location',
    )
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    # Optional: quick status change from admin
    actions = ['mark_as_accepted', 'mark_as_rejected']

    @admin.action(description="Mark selected requests as Accepted")
    def mark_as_accepted(self, request, queryset):
        queryset.update(status='accepted')

    @admin.action(description="Mark selected requests as Rejected")
    def mark_as_rejected(self, request, queryset):
        queryset.update(status='rejected')


# ---------------------------------
# About Us Admin
# ---------------------------------
@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'updated_at',
    )
    search_fields = ('title',)
    ordering = ('-updated_at',)
