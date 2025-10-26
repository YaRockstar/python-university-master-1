from config import db_config as config
from config import queries
from utils import validator


def add_contact(name, phone, email=None):
    """Добавление контакта в телефонную книгу"""
    email = validator.validate_email(email)
    with config.get_connection() as connection:
        cursor = connection.execute(
            queries.INSERT_INTO_CONTACTS,
            (name, phone, email),
        )
        connection.commit()
        return cursor.lastrowid


def get_contacts():
    """Получение списка контактов"""
    with config.get_connection() as connection:
        cursor = connection.execute(queries.SELECT_CONTACTS)
        rows = cursor.fetchall()

    return rows


def get_contact_by_id(contact_id):
    """Получение контакта по id"""
    with config.get_connection() as connection:
        cursor = connection.execute(
            queries.SELECT_CONTACT_BY_ID,
            (contact_id,)
        )
        return cursor.fetchone()


def update_contact(contact_id, name, phone, email):
    """Обновление контакта"""
    email = validator.validate_email(email)
    with config.get_connection() as connection:
        connection.execute(
            queries.UPDATE_CONTACT,
            (name, phone, email, contact_id),
        )
        connection.commit()


def delete_contact(contact_id):
    """Удаление контакта"""
    with config.get_connection() as connection:
        connection.execute(
            queries.DELETE_CONTACT_BY_ID,
            (contact_id,),
        )
        connection.commit()
