from rest_framework.permissions import BasePermission


class RacePermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.is_staff
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        elif view.action in ['partial_update', 'update', 'destroy']:
            return request.user.is_staff
        else:
            return False
