from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.mail import send_mail

from .models import VetRequest, AboutUs, UserProfile
from .serializers import SignupSerializer, VetRequestSerializer, AboutUsSerializer

# ------------------------------------------
# 1. Signup
# ------------------------------------------
class SignupViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

# ------------------------------------------
# 2. Request for Vet Doctor
# ------------------------------------------
class VetRequestViewSet(viewsets.ModelViewSet):
    queryset = VetRequest.objects.all()
    serializer_class = VetRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)

    # GET: /vetrequests/myrequests/
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def myrequests(self, request):
        qs = VetRequest.objects.filter(farmer=request.user)
        serializer = VetRequestSerializer(qs, many=True)
        return Response(serializer.data)

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
                message=f"Click the link to reset your password: {reset_link}",
                from_email="noreply@krishi.com",
                recipient_list=[email],
            )
            return Response({"message": "Password reset link sent!"})

        except User.DoesNotExist:
            return Response({"error": "Email not found"}, status=404)
