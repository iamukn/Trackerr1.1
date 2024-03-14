#!/usr/bin/env python3
from rest_framework import permissions

"""
 Business owner access only

"""

class IsBusinessOwner(permissions.BasePermission):
    """
    Grants access to only business owners
    """
    message = "Restricted to only business owners"

    def has_permission(self, request, view):
        if request.user.account_type == 'business' and request.user.is_authenticated:
            return True
    
#    def has_object_permission(self, request,obj, view):
#        pass
