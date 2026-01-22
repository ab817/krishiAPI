from rest_framework import viewsets, status, generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.mail import send_mail

from .models import VetRequest, AboutUs, NewsArticle
from .serializers import (
    SignupSerializer,
    VetRequestSerializer,
    AboutUsSerializer, NewsArticleSerializer
)
from .permissions import IsAdminUserRole, IsNormalUserRole


# ------------------------------------------
# 1. Signup
# ------------------------------------------
class SignupViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer


# ------------------------------------------
# 2. Vet Request
# ------------------------------------------
class VetRequestViewSet(viewsets.ModelViewSet):
    serializer_class = VetRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Admin → all requests
        if user.profile.role == 'admin':
            return VetRequest.objects.all()

        # Normal → own requests
        return VetRequest.objects.filter(farmer=user)

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)

    # Normal user → view own requests
    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated, IsNormalUserRole]
    )
    def myrequests(self, request):
        qs = VetRequest.objects.filter(farmer=request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    # Admin → accept request
    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated, IsAdminUserRole]
    )
    def accept(self, request, pk=None):
        vet_request = self.get_object()
        vet_request.status = 'accepted'
        vet_request.save()
        return Response({"message": "Request accepted"})

    # Admin → reject request
    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated, IsAdminUserRole]
    )
    def reject(self, request, pk=None):
        vet_request = self.get_object()
        vet_request.status = 'rejected'
        vet_request.save()
        return Response({"message": "Request rejected"})


# ------------------------------------------
# 3. About Us
# ------------------------------------------
class AboutUsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer


# ------------------------------------------
# 4. Password Reset via Email
# ------------------------------------------
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

class PasswordResetViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def send_reset_email(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_link = f"http://yourfrontend.com/reset-password/{uid}/{token}/"

            send_mail(
                subject="Krishi App Password Reset",
                message=f"Click the link to reset your password:\n{reset_link}",
                from_email="noreply@krishi.com",
                recipient_list=[email],
            )
            return Response({"message": "Password reset link sent!"})

        except User.DoesNotExist:
            return Response({"error": "Email not found"}, status=404)

#newsarticle

class NewsArticleViewSet(viewsets.ModelViewSet):
    queryset = NewsArticle.objects.all().order_by('-date')
    serializer_class = NewsArticleSerializer

    def get_permissions(self):
        # Anyone can view news
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        # Only admin can create/update/delete
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated:
            serializer.save(posted_by_user=user)
        else:
            serializer.save(posted_by_name="Admin")