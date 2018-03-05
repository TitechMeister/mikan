from rest_framework import permissions


class WorkAccessPermisson(permissions.BasePermission):
    """
    Permisson for Work.

    - Only users have "create_work_universally"
      can create work from felica_idm
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
            if (not request.user.has_perm("work.create_work_universally")
                    and request.data.get("felica_idm")):
                return False
            # Continue to object level permission check
            else:
                return True

    def has_object_permission(self, request, view, obj):
        """
        Object level permission for Work.

        - Users have permission "work.create_work_universally"
          can write any work.
        - Otherwise, users can only write their own work.
        """
        if request.user.has_perm("work.create_work_universally"):
            return True

        # Read permissions(GET, HEAD, OPTION) are allowed to any request,
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.member == request.user
