#!/usr/bin/env python3
from rest_framework import permissions


"""
 Logistics Partner access only

"""

class IsRider(permissions.BasePermission):
    """
    Grants access to only logistics partner
    """
    message = "logistics partner only!!"

    def has_permission(self, request, view):

        if not request.user.id:
            return False

        elif request.user.account_type == 'logistics' and \
                request.user.is_authenticated: \
            return True
        return False

    def has_object_permission(self, request,obj, view):

       return bool(request.user and request.user.is_authenticated)
