from work.views import ActivityViewSet


work_list = ActivityViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
work_detail = ActivityViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

workplace_list = ActivityViewSet.as_view({
    'get': 'list',
})
workplace_detail = ActivityViewSet.as_view({
    'get': 'retrieve',
})
