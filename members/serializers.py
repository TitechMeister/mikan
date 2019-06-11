from rest_framework import serializers
from members.models import Member, Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ("id", "uid",
                  "username", "email",
                  "first_name", "last_name",
                  "ja_first_name", "ja_last_name",
                  "team", "felica_idm", "profile_image", "executive_generation"
                  "is_active", "is_staff")
        read_only_fields = ('is_active', 'is_staff')
        depth = 1


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ("id",
                  "username", "email",
                  "first_name", "last_name",
                  "ja_first_name", "ja_last_name",
                  "team", "felica_idm", "profile_image")
        depth = 1
