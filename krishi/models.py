from django.db import models
from django.contrib.auth.models import User


# ------------------------------------------
# USER PROFILE
# ------------------------------------------
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('normal', 'Farmer'),
        ('admin', 'Doctor'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    mobile_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='normal')

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# ------------------------------------------
# ANIMAL TYPE
# ------------------------------------------
class AnimalType(models.Model):
    animal_name = models.CharField(max_length=100, unique=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['animal_name']

    def __str__(self):
        return self.animal_name


# ------------------------------------------
# VET REQUEST
# ------------------------------------------
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

    animal_type = models.ForeignKey(
        AnimalType,
        on_delete=models.PROTECT,
        related_name='vet_requests'
    )

    symptoms = models.TextField()
    location = models.CharField(max_length=255)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Request #{self.id} - {self.status}"


# ------------------------------------------
# AUDIT LOG
# ------------------------------------------
class VetRequestLog(models.Model):

    ACTION_CHOICES = (
        ('created', 'Created'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('farmer_cancelled', 'Farmer Cancelled'),
        ('doctor_cancelled', 'Doctor Cancelled'),
    )

    vet_request = models.ForeignKey(
        VetRequest,
        on_delete=models.CASCADE,
        related_name='logs'
    )

    action = models.CharField(max_length=30, choices=ACTION_CHOICES)

    performed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    previous_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Log {self.vet_request.id} - {self.action}"


# ------------------------------------------
# ABOUT US (UNCHANGED)
# ------------------------------------------
class AboutUs(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# ------------------------------------------
# NEWS ARTICLE (UNCHANGED)
# ------------------------------------------
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
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
