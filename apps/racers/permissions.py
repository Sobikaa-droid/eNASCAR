from rest_framework import permissions
from rest_framework.permissions import BasePermission


class RacerPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'POST', 'OPTIONS', 'HEAD']:
            return True
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        if request.method in ['GET', 'OPTIONS', 'HEAD']:
            return True
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user.is_staff or request.user == obj
