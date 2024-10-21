from rest_framework import permissions


class IsReadOnly(permissions.BasePermission):
    """Переопределение базового класса привилегий"""
    def has_permission(self, request, view):
        """Возвращает булевое значение, если методы являются безопасными с точки зрения целостности данных"""
        return request.method in permissions.SAFE_METHODS


class IsHabitOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """Возвращает булевое значение, если тот, кто удаляет объект является его создателем"""
        return request.user == view.queryset.model.objects.get(pk=view.kwargs.get('pk')).user
