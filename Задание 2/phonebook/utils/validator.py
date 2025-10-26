import re

EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


def validate_email(email):
    """Проверка email пользователя на валидность"""
    if email is None or email.strip() == "":
        return None

    email = email.strip()
    if not EMAIL_REGEX.match(email):
        raise ValueError("Неверный формат email")

    return email
