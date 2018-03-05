from work.views import WorkViewSet


work_list = WorkViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
work_detail = WorkViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

workplace_list = WorkViewSet.as_view({
    'get': 'list',
})
workplace_detail = WorkViewSet.as_view({
    'get': 'retrieve',
})
