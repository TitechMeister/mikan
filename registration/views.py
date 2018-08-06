from rest_framework import generics, permissions, parsers
from rest_framework.response import Response
from members.models import Member
from members.serializers import MemberSerializer
from registration.serializers import RegistrationDataSerializer
from registration.models import RegistrationCode


class RegistrationView(generics.CreateAPIView):
    """
    post:
    Register new member.
    """
    queryset = Member.objects.all()
    serializer_class = RegistrationDataSerializer
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser)

    def post(self, request, format=None):
        serializer = RegistrationDataSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.save()

        raw_code = request.data["registration_code"]
        raw_password = request.data["password"]

        used_code_set = RegistrationCode.objects.filter(code=raw_code)
        if used_code_set[0].onetime:
            used_code_set.delete()

        new_user.set_password(raw_password)
#         new_user.is_active = False
        new_user.save()
#         new_user.email_user("hello", "po")

        return Response(MemberSerializer(new_user).data)
