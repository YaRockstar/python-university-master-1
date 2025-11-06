import sqlite3

from . import queries

DB_NAME = "expenses.db"


def get_connection():
    """Предоставление коннекшена к БД"""
    return sqlite3.connect(DB_NAME)


def init_db():
    """Инициализация БД"""
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.executescript(f"""
            {queries.CREATE_EXPENSE_TABLE}
            {queries.CREATE_EXPENSE_AMOUNT_TABLE}
            {queries.CREATE_EXPENSE_DATE_TABLE}
            {queries.CREATE_EXPENSE_DESCRIPTION_TABLE}
            {queries.CREATE_CATEGORY_KNOT_TABLE}
            {queries.CREATE_EXPENSE_CATEGORY_TABLE}
        """)
        connection.commit()
