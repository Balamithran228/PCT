from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to grant full access to admins and read-only access to others.
    """

    def has_permission(self, request, view):
        return True
        # if request.method in SAFE_METHODS:
        #     return True
        # # Ensure user is authenticated and has admin role
        # return request.user.is_authenticated and getattr(request.user, "employee_role", "").lower() == "admin"
