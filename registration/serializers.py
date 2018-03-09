from datetime import datetime
from django.utils import timezone
from rest_framework import serializers
from registration.models import RegistrationCode
from members.models import Member


class RegistrationDataSerializer(serializers.ModelSerializer):
    # Explicitly declare some fields to make them necessary
    password = serializers.CharField(
        style={'input_type': 'password'}
    )
    email = serializers.EmailField()

    first_name = serializers.CharField(max_length=16)
    last_name = serializers.CharField(max_length=16)

    ja_first_name = serializers.CharField(max_length=16)
    ja_last_name = serializers.CharField(max_length=16)

    executive_generation = serializers.IntegerField(min_value=2000,
                                                    max_value=2100)
    registration_code = serializers.CharField(max_length=10)

    def validate_registration_code(self, value):
        try:
            code = RegistrationCode.objects.get(code=value)
        except RegistrationCode.DoesNotExist:
            raise serializers.ValidationError("Invalid registration code.")
        if code.valid_until and code.valid_until < timezone.now():
            raise serializers.ValidationError("This code is no longer valid.")

    def create(self, validated_data):
        validated_data.pop("registration_code", None)
        validated_data.pop("password", None)
        new_user = Member.objects.create(**validated_data)
        return new_user

    class Meta:
        model = Member
        fields = ("username", "email", "password",
                  "first_name", "last_name",
                  "ja_first_name", "ja_last_name",
                  "team", "profile_image",
                  "executive_generation",
                  "registration_code")
