import csv
import json

from config import db_config as config
from config import queries as queries
from utils import helper
from utils import validator


def import_contacts_from_json(filepath, skip_duplicates=True):
    """Импорт контактов из JSON"""
    if not helper.check_file_exists(filepath):
        return

    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    count = 0
    with config.get_connection() as connection:
        for item in data:
            name = item.get("name").strip()
            phone = item.get("phone").strip()
            email = item.get("email")

            if email is not None:
                email = email.strip()

            if not name or not phone:
                continue

            if skip_duplicates:
                cursor = connection.execute(
                    queries.SELECT_CONTACT_BY_NAME_AND_PHONE,
                    (name, phone),
                )
                if cursor.fetchone():
                    continue
            try:
                email = validator.validate_email(email)
            except ValueError:
                email = None

            connection.execute(
                queries.INSERT_INTO_CONTACTS,
                (name, phone, email),
            )
            count += 1
        connection.commit()

    print(f"Импортировано {count} контактов из {filepath}")


def import_contacts_from_csv(filepath, skip_duplicates=True):
    """Импорт контактов из CSV"""
    if not helper.check_file_exists(filepath):
        return

    count = 0
    with open(filepath, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        with config.get_connection() as connection:
            for row in reader:
                name = row.get("name") or row.get("Имя") or row.get("Name")
                phone = row.get("phone") or row.get("Телефон") or row.get("Phone")
                email = row.get("email") or row.get("Email")
                if not name or not phone:
                    continue

                if skip_duplicates:
                    cursor = connection.execute(
                        queries.SELECT_CONTACT_BY_NAME_AND_PHONE,
                        (name, phone),
                    )
                    if cursor.fetchone():
                        continue

                try:
                    email = validator.validate_email(email)
                except ValueError:
                    email = None
                connection.execute(
                    queries.INSERT_INTO_CONTACTS,
                    (name, phone, email),
                )
                count += 1
            connection.commit()

    print(f"Импортировано {count} контактов из {filepath}")
