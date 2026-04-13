from django.utils import timezone
from rest_framework.permissions import BasePermission, SAFE_METHODS


error_message = 'Недостаточно прав.' + ' %(class)s.__doc__'


class SuperuserCRUD(BasePermission):
    """Доступно только SU."""

    message = error_message

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_superuser


class SuperuserCUDAuthRetrievePublished(BasePermission):
    """
    Создать, изменить и удалить может только SU,
    просмотреть опубликованные - любой авторизованный.
    """

    message = error_message

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS and obj.published_at <= timezone.now():
            return True

        return request.user.is_authenticated and request.user.is_superuser
