from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Разрешаем доступ для безопасных методов
        if request.method in SAFE_METHODS:
            return True
        # Проверяем, что ID партнера совпадает с ID текущего пользователя
        return obj.id == request.user.id
