from typing import List


class User:
    """Модель пользователя системы."""

    def __init__(self, username: str, roles: List[str]) -> None:
        """Инициализация пользователя системы."""
        self.username = username
        self.roles = roles
