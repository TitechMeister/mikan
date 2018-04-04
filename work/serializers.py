from rest_framework import serializers
from work.models import Workplace, Activity, Work, WorkPlan, PracticalWork
from members.serializers import MemberSerializer
from members.models import Member


class WorkplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workplace
        fields = "__all__"


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ("id", "member", "workplace",
                  "start_at", "end_at", "is_just_staying")


class CreateActivitySerializerAllowsFelicaIDm(serializers.ModelSerializer):
    """
    A serizlizer for work that allows create work with felica IDm.

    "member" field is automatically provided.
    If "felica_idm" is provided, it will use
    "felica_idm" rather than "member".
    Note that users without special permission are not allowed to access
    this serializer with felica idm.
    """
    felica_idm = serializers.CharField(max_length=16,
                                       min_length=16,
                                       required=False)
    member = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all(),
                                                required=False)

    def validate_felica_idm(self, value):
        """
        Check that the felica idm is registered.
        """
        try:
            Member.objects.get(felica_idm=value)
        except Member.DoesNotExist:
            raise serializers.ValidationError(
                "This Felica IDm are not registered."
            )
        return value

    def create(self, validated_data):
        felica_idm = validated_data.pop("felica_idm", None)
        if felica_idm:
            felica_owner = Member.objects.get(felica_idm=felica_idm)
            del validated_data["member"]
            return Activity.objects.create(member=felica_owner,
                                           **validated_data)
        else:
            return Activity.objects.create(**validated_data)

    class Meta:
        model = Activity
        fields = ("id", "member", "felica_idm", "workplace",
                  "start_at", "end_at", "is_just_staying")


class ActivitySerializerDetailed(serializers.ModelSerializer):
    workplace = WorkplaceSerializer()
    member = MemberSerializer()

    class Meta:
        model = Activity
        fields = ("id", "member", "workplace",
                  "start_at", "end_at", "is_just_staying")


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = "__all__"
        depth = 1


class WorkPlanSerializer(serializers.ModelSerializer):
    completed_by = MemberSerializer()

    class Meta:
        model = WorkPlan
        fields = "__all__"
        depth = 1


class PracticalWorkSerializer(serializers.ModelSerializer):
    work = serializers.PrimaryKeyRelatedField(queryset=Work.objects.all())
    workplace = serializers.PrimaryKeyRelatedField(queryset=Workplace.objects.all()) # noqa

    class Meta:
        model = PracticalWork
        fields = ("work", "workplace")


class CreateWorkPlanSerializer(serializers.ModelSerializer):
    work = PracticalWorkSerializer(many=True)

    def create(self, validated_data):
        practical_work_list = validated_data.pop("work", None)

        new_workplan = super().create(validated_data)

        for practical_work in practical_work_list:
            practical_work["workplan"] = new_workplan
            new_practical_work = PracticalWork.objects.create(**practical_work)
            new_practical_work.save()

        return new_workplan

    class Meta:
        model = WorkPlan
        fields = "__all__"
