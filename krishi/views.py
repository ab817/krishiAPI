from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import (
    VetRequest,
    AnimalType,
    VetRequestLog,
    AboutUs,
    NewsArticle
)
from .serializers import (
    VetRequestSerializer,
    AnimalTypeSerializer,
    AboutUsSerializer,
    NewsArticleSerializer,
    SignupSerializer
)
from .permissions import IsAdminUserRole, IsNormalUserRole
from rest_framework.viewsets import ViewSet
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.contrib.auth.models import User


# ------------------------------------------
# SIGNUP
# ------------------------------------------
class SignupViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer


# ------------------------------------------
# VET REQUEST
# ------------------------------------------
class VetRequestViewSet(viewsets.ModelViewSet):
    serializer_class = VetRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.profile.role == 'admin':
            return VetRequest.objects.all()
        return VetRequest.objects.filter(farmer=user)

    def perform_create(self, serializer):
        vet_request = serializer.save(farmer=self.request.user)

        VetRequestLog.objects.create(
            vet_request=vet_request,
            action='created',
            performed_by=self.request.user,
            previous_status='none',
            new_status='pending'
        )

    # ACCEPT
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUserRole])
    def accept(self, request, pk=None):

        with transaction.atomic():
            vet_request = VetRequest.objects.select_for_update().get(pk=pk)

            if vet_request.status not in ['pending', 'doctor_cancelled']:
                return Response({"error": "Cannot accept this request"}, status=400)

            old_status = vet_request.status

            vet_request.status = 'accepted'
            vet_request.assigned_doctor = request.user
            vet_request.save()

            VetRequestLog.objects.create(
                vet_request=vet_request,
                action='accepted',
                performed_by=request.user,
                previous_status=old_status,
                new_status='accepted'
            )

        return Response({"message": "Request accepted"})

    # REJECT
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUserRole])
    def reject(self, request, pk=None):

        vet_request = self.get_object()

        if vet_request.status != 'pending':
            return Response({"error": "Only pending requests can be rejected"}, status=400)

        old_status = vet_request.status
        vet_request.status = 'rejected'
        vet_request.save()

        VetRequestLog.objects.create(
            vet_request=vet_request,
            action='rejected',
            performed_by=request.user,
            previous_status=old_status,
            new_status='rejected'
        )

        return Response({"message": "Request rejected"})

    # FARMER CANCEL
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsNormalUserRole])
    def farmer_cancel(self, request, pk=None):

        vet_request = self.get_object()

        if vet_request.farmer != request.user:
            return Response({"error": "Not allowed"}, status=403)

        if vet_request.status != 'pending':
            return Response({"error": "Only pending requests can be cancelled"}, status=400)

        old_status = vet_request.status
        vet_request.status = 'cancelled'
        vet_request.save()

        VetRequestLog.objects.create(
            vet_request=vet_request,
            action='farmer_cancelled',
            performed_by=request.user,
            previous_status=old_status,
            new_status='cancelled'
        )

        return Response({"message": "Request cancelled successfully"})

    # DOCTOR CANCEL
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUserRole])
    def doctor_cancel(self, request, pk=None):

        with transaction.atomic():
            vet_request = VetRequest.objects.select_for_update().get(pk=pk)

            if vet_request.status != 'accepted':
                return Response({"error": "Only accepted requests can be cancelled"}, status=400)

            if vet_request.assigned_doctor != request.user:
                return Response({"error": "Only assigned doctor can cancel"}, status=403)

            old_status = vet_request.status

            vet_request.status = 'doctor_cancelled'
            vet_request.assigned_doctor = None
            vet_request.save()

            VetRequestLog.objects.create(
                vet_request=vet_request,
                action='doctor_cancelled',
                performed_by=request.user,
                previous_status=old_status,
                new_status='doctor_cancelled'
            )

        return Response({"message": "Acceptance cancelled. Request reopened."})


# ------------------------------------------
# ANIMAL TYPE
# ------------------------------------------
class AnimalTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AnimalType.objects.all()
    serializer_class = AnimalTypeSerializer
    permission_classes = [permissions.AllowAny]


# ------------------------------------------
# ABOUT US
# ------------------------------------------
class AboutUsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    permission_classes = [permissions.AllowAny]


# ------------------------------------------
# NEWS
# ------------------------------------------
class NewsArticleViewSet(viewsets.ModelViewSet):
    queryset = NewsArticle.objects.all().order_by('-date')
    serializer_class = NewsArticleSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated:
            serializer.save(posted_by_user=user)
        else:
            serializer.save(posted_by_name="Admin")


# ------------------------------------------
# PASSWORD RESET



class PasswordResetViewSet(ViewSet):

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
