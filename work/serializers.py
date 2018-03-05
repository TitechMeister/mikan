from rest_framework import serializers
from work.models import Work, Workplace
from members.serializers import MemberSerializer
from members.models import Member


class WorkplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workplace
        fields = "__all__"


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ("id", "member", "workplace",
                  "start_at", "end_at", "is_just_staying")


class CreateWorkSerializerAllowsFelicaIDm(serializers.ModelSerializer):
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
            return Work.objects.create(member=felica_owner, **validated_data)
        else:
            return Work.objects.create(**validated_data)

    class Meta:
        model = Work
        fields = ("id", "member", "felica_idm", "workplace",
                  "start_at", "end_at", "is_just_staying")


class WorkSerializerDetailed(serializers.ModelSerializer):
    workplace = WorkplaceSerializer()
    member = MemberSerializer()

    class Meta:
        model = Work
        fields = ("id", "member", "workplace",
                  "start_at", "end_at", "is_just_staying")
