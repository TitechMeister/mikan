from rest_framework import generics
from rest_framework.response import Response
from members.models import Member
from members.serializers import MemberSerializer


class AccountInfoRetrieveView(generics.RetrieveAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def get(self, request, format=None):
        serializer = MemberSerializer(request.user, many=False)
        return Response(serializer.data)
