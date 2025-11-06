from datetime import datetime


def validate_date(expense_date):
    """Проверка даты расхода пользователя на валидность"""
    try:
        datetime.strptime(expense_date, "%Y-%m-%d")
        return expense_date
    except ValueError:
        raise ValueError("Дата должна быть в формате ГГГГ-ММ-ДД")
