from datetime import datetime

from config import queries


def add_expense(connection, amount, expense_date, category, description):
    """Добавление расхода в дневник"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    expense_id = _insert_expense(connection)
    _insert_amount(connection, expense_id, amount, timestamp)
    _insert_date(connection, expense_id, expense_date, timestamp)
    if description:
        _insert_description(connection, expense_id, description, timestamp)

    category_id, _ = _ensure_category(connection, category.strip().lower())
    _insert_category(connection, expense_id, category_id, timestamp)

    return expense_id


def get_all_expenses(connection):
    """Получение списка всех расходов"""
    cursor = connection.execute(queries.SELECT_ALL_EXPENSES)
    expenses = cursor.fetchall()

    return expenses


def get_expenses_by_date(connection, date):
    """Получение списка расходов по конкретной дате"""
    cursor = connection.execute(
        queries.SELECT_EXPENSE_BY_DATE,
        (date,)
    )
    expenses = cursor.fetchall()

    return expenses


def get_expenses_by_category(connection, category_name):
    """Получение списка расходов по категории"""
    cursor = connection.execute(
        queries.SELECT_EXPENSE_BY_CATEGORY,
        (category_name,)
    )
    expenses = cursor.fetchall()

    return expenses


def get_expense_by_id(connection, expense_id):
    """Получение расхода по id"""
    cursor = connection.execute(
        queries.SELECT_EXPENSE_BY_ID,
        (expense_id,)
    )
    return cursor.fetchone()


def _insert_expense(connection):
    """Добавление расхода"""
    cur = connection.cursor()
    cur.execute(queries.INSERT_INTO_EXPENSE)
    return cur.lastrowid


def _insert_amount(connection, expense_id, amount, timestamp):
    """Заполнение суммы у расхода"""
    connection.execute(
        queries.INSERT_INTO_EXPENSE_AMOUNT,
        (expense_id, amount, timestamp),
    )


def _insert_date(connection, expense_id, date_value, timestamp):
    """Заполнение даты у расхода"""
    connection.execute(
        queries.INSERT_INTO_EXPENSE_DATE,
        (expense_id, date_value, timestamp),
    )


def _insert_description(connection, expense_id, description, timestamp):
    """Заполнение описания у расхода"""
    connection.execute(
        queries.INSERT_INTO_EXPENSE_DESCRIPTION,
        (expense_id, description, timestamp),
    )


def _ensure_category(connection, category):
    """Добавление категории"""
    connection.execute(queries.INSERT_INTO_CATEGORY_KNOT, (category,))
    cur = connection.execute(queries.SELECT_CATEGORY_BY_NAME, (category,))
    return cur.fetchone()


def _insert_category(connection, expense_id, category_id, timestamp):
    """Добавление связи между расходом и категорией"""
    connection.execute(
        queries.INSERT_INTO_EXPENSE_CATEGORY,
        (expense_id, category_id, timestamp),
    )
