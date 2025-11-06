import sqlite3

from . import queries

DB_NAME = "phonebook.db"


def get_connection():
    """Предоставление коннекшена к БД"""
    return sqlite3.connect(DB_NAME)


def init_db():
    """Инициализация БД"""
    with get_connection() as connection:
        connection.execute(queries.CREATE_CONTACTS_TABLE)
        connection.commit()
