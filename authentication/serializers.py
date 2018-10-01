from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from members.models import Member

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class AuthenticationSerializer(JSONWebTokenSerializer):
    username_field = 'username_or_email'

    def validate(self, attrs):
        password = attrs.get("password")
        user_obj = (Member.objects.filter(email=attrs.get("username_or_email")).first()        # noqa
                    or Member.objects.filter(username=attrs.get("username_or_email")).first()) # noqa

        if user_obj is None:
            msg = 'Account with this email/username does not exists'
            raise serializers.ValidationError(msg)

        credentials = {
            'username': user_obj.username,
            'password': password
        }

        if not (all(credentials.values())):
            msg = 'Must include "{username_field}" and "password".'
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)

        user = authenticate(**credentials)

        if not user:
            msg = 'Unable to log in with provided credentials.'
            raise serializers.ValidationError(msg)

        if not user.is_active:
            msg = 'User account is disabled.'
            raise serializers.ValidationError(msg)

        payload = jwt_payload_handler(user)

        return {
            'token': jwt_encode_handler(payload),
        }
