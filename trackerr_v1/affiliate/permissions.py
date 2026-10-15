
from rest_framework.permissions import BasePermission


class IsAffiliate(BasePermission):
    message = "Affiliate authentication is required."

    def has_permission(self, request, view):
        return (
            getattr(request.user, "is_authenticated", False)
            and request.user.__class__.__name__ == "Affiliate"
        )
