from rest_framework import permissions


class MemberAccessPermisson(permissions.BasePermission):
    """
    Permisson for Member.

    - Users have permission "member.modify_member_universally"
      can modify members' information
    - Otherwise, users can only modify their own information.
    """
    def has_permission(self, request, view):
        # Authentication is required
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method == "POST" and not request.user.is_staff:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        """
        Object level permission for Member.

        - Admin can modify any member's information
        - Otherwise, users can only write their own work.
        """
        if request.user.is_staff:
            return True

        # Read permissions(GET, HEAD, OPTION) are allowed to any request,
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.id == request.user.id
