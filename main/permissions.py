from rest_framework import permissions


class SelfInstanceAccessPermission(permissions.BasePermission):
    message = 'Access denied.'

    def has_object_permission(self, request, view, obj):
        try:
            if obj.email == request.user.email:
                return True
            return False
        except:
            if obj.user.email == request.user.email:
                return True
            return False


class IsManager(permissions.BasePermission):
    message = 'Access denied.'

    def has_permission(self, request, view):
        return request.user.role == 1

    def has_object_permission(self, request, view, obj):
        if obj._meta.model.__name__ == 'Report' and obj.organization != request.user.organization:
            return False
        return True
