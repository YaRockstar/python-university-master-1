import csv

from config import db_config as config
from config import queries as queries


def export_expenses_to_csv(filepath):
    """Экспорт расходов в CSV"""
    with config.get_connection() as connection:
        count = connection.execute(queries.SELECT_ALL_EXPENSES)
        rows = count.fetchall()

    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "amount", "date", "category", "description"])
        for row in rows:
            writer.writerow(row)

    print(f"Экспортировано {len(rows)} расходов в {filepath}")
