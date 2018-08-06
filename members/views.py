from rest_framework import viewsets, permissions
from members.models import Member, Team
from members.serializers import MemberSerializer, TeamSerializer


class MemberViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given member.

    list:
    Return a list of all the existing members.
    """
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given team.

    list:
    Return a list of all the existing teams.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (permissions.AllowAny,)
