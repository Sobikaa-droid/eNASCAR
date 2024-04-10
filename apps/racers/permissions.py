from rest_framework.permissions import BasePermission


class RacerPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve', 'create']:
            return True
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user.is_staff
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.username == obj.username or request.user.is_staff:
            return True
        else:
            if view.action == 'retrieve':
                return True
            elif view.action in ['partial_update']:
                return set(request.data.keys()) == {'racer'} or request.user.is_staff
            elif view.action in ['update', 'destroy']:
                return request.user.is_staff
            else:
                return False
