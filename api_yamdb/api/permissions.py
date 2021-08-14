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
