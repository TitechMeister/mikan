from datetime import datetime
from django.utils import timezone
from django.db.models import Q
from rest_framework import serializers
from work.models import Activity


class ActivityTimeRangeValidator:
    def __init__(self, member):
        self.member = member

    def __call__(self, start, end):
        now = timezone.now()
        if (type(start) is datetime):
            start_datetime = start
        else:
            start_datetime_native = datetime.strptime(start, '%Y-%m-%dT%H:%M')
            start_datetime = timezone.make_aware(start_datetime_native)
        if start_datetime > now:
            raise serializers.ValidationError(
                "You can't create future activity."
            )
        q_base = Q(member=self.member,
                   end_at__isnull=False)
        # q1: be inside exising activity
        # q2: overlaps with exisiting activity
        if end:
            q_1 = Q(start_at__lt=start,
                    end_at__gt=end)
            q_2 = (Q(start_at__range=(start, end))
                   | Q(end_at__range=(start, end)))
        else:
            q_1 = Q()
            q_2 = Q(end_at__gt=start)

        conflicting = Activity.objects.filter(
            q_base & (q_1 | q_2)
        )
        if conflicting:
            raise serializers.ValidationError(
                "Conflicting activity exist."
            )
