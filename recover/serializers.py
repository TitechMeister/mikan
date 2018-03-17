from django.utils import timezone
from rest_framework import serializers
from members.models import Member
from recover.models import RecoverToken


def validate_recover_token(token):
    instance_set = RecoverToken.objects.filter(token=token)
    if not instance_set:
        raise serializers.ValidationError("This token is invalid.")
    instance = instance_set[0]
    if instance.valid_until < timezone.now():
        instance_set.delete()
        raise serializers.ValidationError("This token is no longer valid.")


class RecoverTokenCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            Member.objects.get(email=value)
        except Member.DoesNotExist:
            error_msg = "User with the email does not exist."
            raise serializers.ValidationError(error_msg)
        return value

    def create(self, validated_data):
        member = Member.objects.get(email=validated_data["email"])
        return RecoverToken.objects.create(member=member)

    class Meta:
        model = RecoverToken
        fields = ("email",)


class RecoverTokenRetriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecoverToken
        fields = ("token", "member")


class VerifyRecoverTokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=30)

    def validate_token(self, value):
        validate_recover_token(value)
        return value

    class Meta:
        model = RecoverToken
        fields = ("token",)


class RenewPasswordSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=128)

    def validate_token(self, value):
        validate_recover_token(value)
        return value

    class Meta:
        model = RecoverToken
        fields = ("token", "password")
