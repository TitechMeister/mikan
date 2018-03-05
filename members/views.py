from rest_framework import viewsets
from members.models import Member
from members.serializers import MemberSerializer, MemberSerializerDetailed
from members.permissions import MemberAccessPermisson


class MemberViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = (MemberAccessPermisson,)

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return MemberSerializerDetailed
        return MemberSerializer
