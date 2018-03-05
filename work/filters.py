from django_filters import rest_framework as filters
from work.models import Work


class WorkFilter(filters.FilterSet):
    in_progress = filters.BooleanFilter(label="Work in progress",
                                        method="filter_in_progress")
    start = filters.DateTimeFromToRangeFilter(field_name="start_at")
    end = filters.DateTimeFromToRangeFilter(field_name="end_at")

    def filter_in_progress(self, queryset, name, value):
        return queryset.filter(end_at__isnull=True)

    class Meta:
        model = Work
        fields = ("member", "workplace", "in_progress", "start", "end")
