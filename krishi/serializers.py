from rest_framework import serializers
from django.contrib.auth.models import User
from .models import VetRequest, AboutUs, UserProfile


# --------------------------
# Signup Serializer
# --------------------------
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    mobile_number = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=['normal', 'admin'], default='normal')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'mobile_number', 'role']

    def validate_mobile_number(self, value):
        if UserProfile.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError("Mobile number already exists")
        return value

    def create(self, validated_data):
        mobile = validated_data.pop('mobile_number')
        role = validated_data.pop('role')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )

        UserProfile.objects.create(
            user=user,
            mobile_number=mobile,
            role=role
        )
        return user


# --------------------------
# Vet Request Serializer
# --------------------------
class VetRequestSerializer(serializers.ModelSerializer):
    farmer_name = serializers.CharField(source='farmer.username', read_only=True)

    class Meta:
        model = VetRequest
        fields = "__all__"
        read_only_fields = ['farmer', 'status', 'created_at']


# --------------------------
# About Us Serializer
# --------------------------
class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = "__all__"
