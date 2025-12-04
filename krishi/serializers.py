from rest_framework import serializers
from django.contrib.auth.models import User
from .models import VetRequest, AboutUs, UserProfile

# --------------------------
# Signup Serializer
# --------------------------
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    mobile_number = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'mobile_number']

    def validate_mobile_number(self, value):
        if UserProfile.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError("Mobile number already exists")
        return value

    def create(self, validated_data):
        mobile = validated_data.pop('mobile_number')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Save mobile number in UserProfile
        UserProfile.objects.create(user=user, mobile_number=mobile)
        return user


# --------------------------
# Vet Request
# --------------------------
class VetRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VetRequest
        fields = "__all__"
        read_only_fields = ['farmer', 'status']


# --------------------------
# About Us
# --------------------------
class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = "__all__"
