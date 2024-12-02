from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


"""
ModelBackend: Это базовый бэкенд аутентификации, предоставляемый Django. 
Он используется для аутентификации пользователей по username и паролю.

get_user_model: Эта функция возвращает активную модель пользователя, которая используется в проекте.

Q: Это класс, используемый для создания сложных запросов к базе данных.
"""

"""
Эта строка получает активную модель пользователя для текущего проекта.
"""
UserModel = get_user_model()


class EmailBackend(ModelBackend):
    """
    Этот класс наследуется от ModelBackend, что позволяет ему использовать все его методы и свойства.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # authenticate: Этот метод вызывается при попытке аутентификации пользователя.
        # request: Объект запроса, который передается методу.
        # username: Имя пользователя (в данном случае email).
        # password: Пароль пользователя.
        # **kwargs: Дополнительные аргументы.
        try:
            # поиск пользователя
            user = UserModel.objects.get(Q(email__iexact=username))
        except UserModel.DoesNotExist:
            return None

        # Проверка пароля и возможности аутентификации
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        # Если пароль неправильный, или пользователь не может быть аутентифицирован, то None
        return None

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None