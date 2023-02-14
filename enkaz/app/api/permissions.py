from rest_framework.permissions import BasePermission

class IsAnonymous(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsAdminUserorIsAnonymous(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or not request.user.is_authenticated

class IsAdminUserorIsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff