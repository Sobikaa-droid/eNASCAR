from rest_framework.permissions import BasePermission


class CarModelPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'OPTIONS', 'HEAD']:
            return True
        elif request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user.is_staff


class CarPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'OPTIONS', 'HEAD']:
            return True
        elif request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user.is_authenticated and not request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'OPTIONS', 'HEAD']:
            return True
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user == obj
