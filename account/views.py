from rest_framework import generics
from rest_framework.response import Response
from members.models import Member
from members.serializers import AccountSerializer


class AccountInfoRetrieveView(generics.RetrieveAPIView):
    queryset = Member.objects.all()
    serializer_class = AccountSerializer

    def get(self, request, format=None):
        serializer = AccountSerializer(request.user, many=False)
        return Response(serializer.data)
