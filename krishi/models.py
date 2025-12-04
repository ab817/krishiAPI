from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    mobile_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f"{self.user.username} - {self.mobile_number}"


class VetRequest(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vet_requests")
    animal_type = models.CharField(max_length=100)
    symptoms = models.TextField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.farmer.username} - {self.animal_type}"


class AboutUs(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
