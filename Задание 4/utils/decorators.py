from typing import List, Any

from core.exceptions import PermissionDeniedError


def check_permissions(required_roles: List[str]):
    """Декоратор, проверяющий, что у пользователя есть хотя бы одна требуемая роль."""
    req = set(required_roles)

    def decorator(func):
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Импорты внутри функции для избежания циклических зависимостей.
            from domain.user import User
            from application.services.transport_company import TransportCompany

            user = kwargs.get("user")
            if user is None:
                if len(args) > 1 and isinstance(args[0], TransportCompany) and isinstance(args[1], User):
                    user = args[1]

            if user is None or not isinstance(user, User):
                raise PermissionDeniedError("Отсутствует пользователь для проверки прав.")

            if not (set(user.roles) & req):
                raise PermissionDeniedError(f"Недостаточно прав. Требуются роли из: {sorted(req)}")

            return func(*args, **kwargs)

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper

    return decorator
