from django.utils import timezone
from rest_framework import viewsets
from work.models import Work, Workplace
from work.serializers import (
    WorkSerializer,
    WorkSerializerDetailed,
    CreateWorkSerializerAllowsFelicaIDm,
    WorkplaceSerializer
)
from work.validators import WorkTimeRangeValidator
from work.filters import WorkFilter
from work.permissions import WorkAccessPermisson


class WorkViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Work.objects.all()
    filter_class = WorkFilter
    permission_classes = (WorkAccessPermisson,)

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return WorkSerializerDetailed
        elif self.action == "create":
            return CreateWorkSerializerAllowsFelicaIDm
        return WorkSerializer

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

        validate = WorkTimeRangeValidator(self.request.user)
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
