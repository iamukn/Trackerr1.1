from rest_framework.permissions import BasePermission
from business.views.business_owner_permission import IsBusinessOwner
from logistics.views.logistics_owner_permission import IsLogisticsOwner

class IsBusinessOrLogistics(BasePermission):
    def has_permission(self, request, view):
        return IsBusinessOwner().has_permission(request, view) or \
               IsLogisticsOwner().has_permission(request, view)

