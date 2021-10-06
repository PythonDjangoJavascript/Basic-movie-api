from rest_framework import permissions


class AdminOrReadOnly(permissions.IsAdminUser):
    """Provides permissions to readonly to all and endit create permission to
    Admin user"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        # return super().has_permission(request, view)
        return bool(request.user and request.user.is_staff)


class ReviewOwnerOrReadOnly(permissions.BasePermission):
    """Provies permission to read only to all and edit permissions to
    Review owner only"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.review_user == request.user) or request.user.is_staff
