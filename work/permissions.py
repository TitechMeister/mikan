from rest_framework import permissions


class ActivityAccessPermisson(permissions.BasePermission):
    """
    Permisson for Activity.

    - Only users have "create_activity_universally"
      can create activities from felica_idm
    """
    def has_permission(self, request, view):
        # Authentication is required
        if not (request.user and request.user.is_authenticated):
            return False

        # All authenticated users are allowed to read
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            # users without special permission are
            # not allowed to access with felica idm.
            if (not request.user.has_perm("activity.create_activity_universally")
                    and request.data.get("felica_idm")):
                return False
            # Continue to object level permission check
            else:
                return True

    def has_object_permission(self, request, view, obj):
        """
        Object level permission for Acvtivity.

        - Users have permission "activities.create_activity_universally"
          can write any activities.
        - Otherwise, users can only write their own activities.
        """
        if request.user.has_perm("activity.create_activity_universally"):
            return True

        # Read permissions(GET, HEAD, OPTION) are allowed to any request,
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.member == request.user
