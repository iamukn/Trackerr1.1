#!/usr/bin/python3
from rest_framework.permissions import BasePermission
"""
  Permission that allows only a business or a logistic user 
  to change password
"""

class IsBusinessOrLogisticsOwner(BasePermission):

    message = "Access limited to business and logistics partners only!"

    def has_permission(self, request, view):
        if request.user.account_type == 'business' or request.user.account_type == 'logistics' and request.user.is_authenticated:
            return bool(request.user)
        return False

    def has_obj_permission(self, request, obj, view):
        
        return bool(request.user.is_authenticated and request.user)
