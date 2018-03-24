from django.utils import timezone
from rest_framework import viewsets
from work.models import Activity, Workplace
from work.serializers import (
    ActivitySerializer,
    ActivitySerializerDetailed,
    CreateActivitySerializerAllowsFelicaIDm,
    WorkplaceSerializer
)
from work.validators import ActivityTimeRangeValidator
from work.filters import ActivityFilter
from work.permissions import ActivityAccessPermisson


class ActivityViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Activity.objects.all()
    filter_class = ActivityFilter
    permission_classes = (ActivityAccessPermisson,)

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return ActivitySerializerDetailed
        elif self.action == "create":
            return CreateActivitySerializerAllowsFelicaIDm
        return ActivitySerializer

    def perform_create(self, serializer):
        """
        A function which will be called when objects are saved.

        If "start_at" is not provided, it will use current time.
        If there is a work which is currently in progress,
        its "end_at" is automatically set to new "start_at".
        """
        start_at = self.request.data["start_at"]
        if not start_at:
            start_at = timezone.now()
            start_at = start_at.replace(microsecond=0)
        end_at = self.request.data.get("end_at", None)

        validate = ActivityTimeRangeValidator(self.request.user)
        validate(start_at, end_at)

        work_in_progress = self.queryset.filter(member=self.request.user,
                                                end_at__isnull=True)
        for work in work_in_progress:
            work.end_at = start_at
            work.save()

        serializer.save(member=self.request.user, start_at=start_at)


class WorkplaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Workplace.objects.all()
    serializer_class = WorkplaceSerializer
