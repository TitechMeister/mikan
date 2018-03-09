from members.views import MemberViewSet, TeamViewSet


member_list = MemberViewSet.as_view({
    'get': 'list'
})
member_detail = MemberViewSet.as_view({
    'get': 'retrieve'
})

team_list = TeamViewSet.as_view({
    'get': 'list'
})
team_detail = TeamViewSet.as_view({
    'get': 'retrieve'
})
