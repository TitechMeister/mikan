from rest_framework import generics
from rest_framework.response import Response
from members.models import Member
from members.serializers import MemberSerializerDetailed


class AccountInfoRetrieveView(generics.RetrieveAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializerDetailed

    def get(self, request, format=None):
        serializer = MemberSerializerDetailed(request.user, many=False)
        return Response(serializer.data)
