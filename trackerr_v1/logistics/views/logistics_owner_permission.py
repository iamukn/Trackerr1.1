#!/usr/bin/env python3
from rest_framework import permissions
from django.urls.exceptions import Http404
from django.contrib.auth.models import AnonymousUser
"""
 Business owner access only

"""

class IsLogisticsOwner(permissions.BasePermission):
    """
    Grants access to only business owners
    """
    message = "Restricted to only logistics partner"

    def has_permission(self, request, view):

        if not request.user.id:
            return False

        elif request.user.account_type == 'logistics' and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request,obj, view):

       return bool(request.user and request.user.is_authenticated)
