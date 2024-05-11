from rest_framework.permissions import BasePermission


class RacerPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'POST', 'OPTIONS', 'HEAD']:
            return True
        elif request.method in ['PUT', 'PATCH']:
            return request.user.is_authenticated
        elif request.method == 'DELETE':
            return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'OPTIONS', 'HEAD']:
            return True
        elif request.method in ['PUT', 'PATCH']:
            return request.user.is_staff or request.user == obj
        elif request.method == 'DELETE':
            return request.user.is_staff
