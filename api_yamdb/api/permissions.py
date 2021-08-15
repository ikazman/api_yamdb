from rest_framework import permissions


class OwnerOrReadOnly(permissions.BasePermission):
    message = "Изменение чужого контента запрещено!"

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class Moderator(permissions.BasePermission):
    message = "Изменение чужого контента разрешено!"

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user == 'moderator')


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_staff
                    or request.user.role == 'admin'
                    or request.user.is_superuser)
        return False

    def has_object_permission(self, request, view, obj):
        if (request.user.is_authenticated
                and request.user.role == 'admin'
                or request.user.is_staff):
            return True


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        return request.method in permissions.SAFE_METHODS


class IsAuthorOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (obj.author == request.user
                    or request.user.role == 'moderator'
                    or request.user.role == 'admin')
        return request.method in permissions.SAFE_METHODS
