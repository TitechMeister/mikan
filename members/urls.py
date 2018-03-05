from members.views import MemberViewSet


member_list = MemberViewSet.as_view({
    'get': 'list'
})
member_detail = MemberViewSet.as_view({
    'get': 'retrieve'
})
