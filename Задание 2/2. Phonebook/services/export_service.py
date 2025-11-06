import csv
import json

from config import db_config as config
from config import queries as queries


def export_contacts_to_json(filepath):
    """Экспорт контактов в JSON"""
    with config.get_connection() as connection:
        count = connection.execute(queries.SELECT_CONTACTS)
        rows = count.fetchall()

    data = []
    for row in rows:
        contact_id, name, phone, email = row
        data.append({"id": contact_id, "name": name, "phone": phone, "email": email})

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Экспортировано {len(data)} контактов в {filepath}")


def export_contacts_to_csv(filepath):
    """Экспорт контактов в CSV"""
    with config.get_connection() as connection:
        count = connection.execute(queries.SELECT_CONTACTS)
        rows = count.fetchall()

    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "name", "phone", "email"])
        for row in rows:
            writer.writerow(row)

    print(f"Экспортировано {len(rows)} контактов в {filepath}")
