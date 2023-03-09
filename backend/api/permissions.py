from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticatedOrReadOnly)


class IsAdminOrReadOnly(BasePermission):
    """Изменения только для админов, богоподобно"""
    def has_permission(self, request, view):
        return (
            request.method in ('GET',)
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuthorAdminOrReadOnly(IsAuthenticatedOrReadOnly):
    """Автор изменяет свое добро, админ как читер, др ток чтение"""
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and (request.user.is_superuser
                                              or obj.author == request.user
                                              or request.method == 'POST'):
            return True
        return request.method in SAFE_METHODS


class IsAuthUserOrAdminOrReadOnly(IsAuthenticatedOrReadOnly):
    """Админ читер, юзеры могут менять подписки избранное"""
    def has_object_permission(self, request, view, obj):
        return (
            request.method in ('GET',)
            or (request.user == obj)
            or request.user.is_admin
        )
