"""User permission classes."""

from rest_framework.permissions import BasePermission


class IsHisUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user
