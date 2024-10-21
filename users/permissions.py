from rest_framework import permissions


class IsOwnerOrSuperUser(permissions.BasePermission):
    """Класс для проверки привилегия на уровне пользователя"""
    def has_object_permission(self, request, view, obj):
        """Возвращает булевое значение, если тот, кто удаляет объект является его создателем или суперпользователем"""
        return request.user == obj or request.user.is_superuser
