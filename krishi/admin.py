from django.contrib import admin
from .models import VetRequest, AboutUs, UserProfile, NewsArticle, AnimalType


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
# Animal Type Admin
# ---------------------------------
@admin.register(AnimalType)
class AnimalTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'animal_name', 'remarks')
    search_fields = ('animal_name',)
    ordering = ('animal_name',)


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
        'animal_type__animal_name',
        'location',
    )

    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

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


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'date',
        'posted_by_user',
        'posted_by_name'
    )
    search_fields = ('title', 'description', 'posted_by_name')
    list_filter = ('date',)