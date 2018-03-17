import textwrap
from rest_framework import permissions, views
from rest_framework.response import Response
from django.conf import settings
from recover.models import RecoverToken
from recover.serializers import (
    RecoverTokenCreateSerializer,
    RecoverTokenRetriveSerializer,
    VerifyRecoverTokenSerializer,
    RenewPasswordSerializer
)


class RecoverTokenView(views.APIView):
    serializer_class = RecoverTokenCreateSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = RecoverTokenCreateSerializer(data=request.data,
                                                  many=False)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        mail = textwrap.dedent(f"""\
        Mikanのパスワードをリセットするには、次のリンクにアクセスしてください。

        {settings.PASSWORD_RECOVERY_URL}/{instance.token}

        このリンクは24時間有効です。
        \
        """) + settings.EMAIL_SIGNATURE
        title = settings.EMAIL_TITLE_PREFIX + "Mikanのパスワードリセット"
        instance.member.email_user(title, mail)

        return Response(RecoverTokenRetriveSerializer(instance).data)


class VerifyRecoverTokenView(views.APIView):
    serializer_class = VerifyRecoverTokenSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = VerifyRecoverTokenSerializer(data=request.data,
                                                  many=False)
        serializer.is_valid(raise_exception=True)
        instance = RecoverToken.objects.get(token=request.data["token"])

        return Response(RecoverTokenRetriveSerializer(instance).data)


class RenewPasswordView(views.APIView):
    serializer_class = RenewPasswordSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = RenewPasswordSerializer(data=request.data,
                                             many=False)
        serializer.is_valid(raise_exception=True)

        token_set = RecoverToken.objects.filter(token=request.data["token"])
        token = token_set[0]
        token.member.set_password(request.data["password"])
        token.member.save()
        token_set.delete()

        return Response(RecoverTokenRetriveSerializer(token).data)
