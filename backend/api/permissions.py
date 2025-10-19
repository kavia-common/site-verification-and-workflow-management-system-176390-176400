from rest_framework.permissions import BasePermission, SAFE_METHODS


# PUBLIC_INTERFACE
class IsStaffOrReadOnly(BasePermission):
    """Allow read-only for authenticated users; staff can create/update/delete."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)
