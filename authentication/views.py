from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from authentication.serializers import AuthenticationSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class AuthView(GenericAPIView):
    serializer_class = AuthenticationSerializer

    def post(self, request):
        serializer = AuthenticationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.data)
        if not user:
            raise AuthenticationFailed()
        # 以下2行が今回のカスタマイズ部分
        if user.company != serializer.data['company']:
            raise AuthenticationFailed()
        payload = jwt_payload_handler(user)
        return Response({
            'token': jwt_encode_handler(payload),
        })
