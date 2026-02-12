from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('normal', 'Normal User'),   # Farmer
        ('admin', 'Admin User'),     # Vet/Doctor
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    mobile_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='normal')

    def __str__(self):
        return f"{self.user.username} ({self.role})"

#animaltype
class AnimalType(models.Model):
    animal_name = models.CharField(max_length=100, unique=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Animal Type"
        verbose_name_plural = "Animal Types"

    def __str__(self):
        return self.animal_name

#vetrequest
from django.db import models
from django.contrib.auth.models import User

class VetRequest(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('doctor_cancelled', 'Doctor Cancelled'),
        ('cancelled', 'Cancelled'),
    )

    farmer = models.ForeignKey(
        User,
        related_name='farmer_requests',
        on_delete=models.CASCADE
    )

    assigned_doctor = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='assigned_requests'
    )

    animal_type = models.CharField(max_length=100)
    symptoms = models.TextField()
    location = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.status}"


# ✅ DO NOT REMOVE (AS REQUESTED)
class AboutUs(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


#news article
class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    picture = models.ImageField(upload_to='news/', blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    posted_by_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='news_articles'
    )
    posted_by_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text="Used when article is not posted by admin user"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title