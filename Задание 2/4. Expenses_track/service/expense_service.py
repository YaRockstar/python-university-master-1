from config import db_config as config
from config import queries
from repository import expense_repository as repository


def add_expense(amount, expense_date, category, description=None):
    """Добавление расхода в дневник"""
    with config.get_connection() as connection:
        try:
            expense_id = repository.add_expense(connection, amount, expense_date, category, description)
            connection.commit()
            print(f"Расход {expense_id} успешно добавлен")
            return expense_id
        except Exception as e:
            connection.rollback()
            print(f"Ошибка при добавлении расхода: {e}")


def get_all_expenses():
    """Получение списка всех расходов"""
    with config.get_connection() as connection:
        expenses = repository.get_all_expenses(connection)

    return expenses


def get_expenses_by_date(date_value):
    """Получение списка расходов по конкретной дате"""
    with config.get_connection() as connection:
        expenses = repository.get_expenses_by_date(connection, date_value)

    return expenses


def get_expenses_by_category(category):
    """Получение списка расходов по категории"""
    with config.get_connection() as connection:
        expenses = repository.get_expenses_by_category(connection, category)

    return expenses


def get_expense_by_id(expense_id):
    """Получение расхода по id"""
    with config.get_connection() as connection:
        return repository.get_expense_by_id(connection, expense_id)
