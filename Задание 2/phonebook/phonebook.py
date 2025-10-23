import sqlite3
import csv
import json
import os
import re


DB_FILENAME = "phonebook.db"

EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


def get_connection():
    """Предоставление коннекшена к БД"""
    return sqlite3.connect(DB_FILENAME)


def init_db():
    """Инициализация БД"""
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT
            )
            """
        )
        connection.commit()


def validate_email(email):
    """Проверка email пользователя на валидность"""
    if email is None or email.strip() == "":
        return None

    email = email.strip()
    if not EMAIL_RE.match(email):
        raise ValueError("Неверный формат email")

    return email


def add_contact(name, phone, email = None):
    """Добавление контакта в телефонную книгу"""
    email = validate_email(email)
    with get_connection() as connection:
        cur = connection.execute(
            "INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
            (name.strip(), phone.strip(), email),
        )
        connection.commit()
        return cur.lastrowid


def get_contacts():
    """Получение списка контактов"""
    with get_connection() as connection:
        cur = connection.execute("SELECT id, name, phone, email FROM contacts ORDER BY name")
        rows = cur.fetchall()

    if not rows:
        print("Контакты отсутствуют")
        return

    print(f"\n{'ID':<4} {'Имя':<30} {'Телефон':<20} {'Email'}")
    print("-" * 70)

    for r in rows:
        id_, name, phone, email = r
        print(f"{id_:<4} {name:<30} {phone:<20} {email or ''}\n")


def get_contact_by_id(contact_id):
    """Получение контакта по id"""
    with get_connection() as connection:
        cur = connection.execute("SELECT id, name, phone, email FROM contacts WHERE id = ?", (contact_id,))
        return cur.fetchone()


def update_contact(contact_id, name, phone, email):
    """Обновление контакта"""
    email = validate_email(email)
    with get_connection() as connection:
        connection.execute(
            "UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?",
            (name.strip(), phone.strip(), email, contact_id),
        )
        connection.commit()


def delete_contact(contact_id):
    """Удаление контакта"""
    with get_connection() as connection:
        connection.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        connection.commit()


def export_json(filepath):
    """Экспорт контактов в JSON"""
    with get_connection() as connection:
        cur = connection.execute("SELECT id, name, phone, email FROM contacts ORDER BY id")
        rows = cur.fetchall()
    data = []
    for r in rows:
        id_, name, phone, email = r
        data.append({"id": id_, "name": name, "phone": phone, "email": email})
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Экспортировано {len(data)} контактов в {filepath}")


def export_csv(filepath):
    """Экспорт контактов в CSV"""
    with get_connection() as connection:
        cur = connection.execute("SELECT id, name, phone, email FROM contacts ORDER BY id")
        rows = cur.fetchall()

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "phone", "email"])
        for r in rows:
            writer.writerow(r)

    print(f"Экспортировано {len(rows)} контактов в {filepath}")


def import_json(filepath, skip_duplicates = True):
    """Импорт контактов из JSON"""
    if not os.path.exists(filepath):
        print("Файл не найден")
        return
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    added = 0
    with get_connection() as connection:
        for item in data:
            name = item.get("name")
            phone = item.get("phone")
            email = item.get("email")
            if not name or not phone:
                continue
            if skip_duplicates:
                cur = connection.execute(
                    "SELECT id FROM contacts WHERE name = ? AND phone = ?",
                    (name.strip(), phone.strip()),
                )
                if cur.fetchone():
                    continue
            try:
                email = validate_email(email)
            except ValueError:
                email = None
            connection.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name.strip(), phone.strip(), email))
            added += 1
        connection.commit()

    print(f"Импортировано {added} контактов из {filepath}")


def import_csv(filepath, skip_duplicates = True):
    """Импорт контактов из CSV"""
    if not os.path.exists(filepath):
        print("Файл не найден")
        return

    added = 0
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        with get_connection() as connection:
            for row in reader:
                name = row.get("name") or row.get("Имя") or row.get("Name")
                phone = row.get("phone") or row.get("Телефон") or row.get("Phone")
                email = row.get("email") or row.get("Email")
                if not name or not phone:
                    continue
                if skip_duplicates:
                    cur = connection.execute("SELECT id FROM contacts WHERE name = ? AND phone = ?", (name.strip(), phone.strip()))
                    if cur.fetchone():
                        continue
                try:
                    email = validate_email(email)
                except ValueError:
                    email = None
                connection.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name.strip(), phone.strip(), email))
                added += 1
            connection.commit()

    print(f"Импортировано {added} контактов из {filepath}")


def prompt_non_empty(prompt_text, default = None):
    """Обработка ввода пользователя"""
    while True:
        val = input(f"{prompt_text}" + (f" [{default}]" if default else "") + ": ")

        if val.strip() == "" and default is not None:
            return default
        if val.strip() == "":
            print("Поле не должно быть пустым")
        else:
            return val.strip()


def show_menu():
    print("""
        ===== Приложение 'Телефонная книга' =====
        1. Добавить контакт
        2. Показать все контакты
        3. Просмотреть контакт по ID
        4. Редактировать контакт
        5. Удалить контакт
        6. Экспорт в JSON
        7. Экспорт в CSV
        8. Импорт из JSON
        9. Импорт из CSV
        0. Выход
""")


def main():
    init_db()
    try:
        while True:
            show_menu()
            choice = input("Выберите пункт: ").strip()
            try:
                if choice == "1":
                    name = prompt_non_empty("Имя")
                    phone = prompt_non_empty("Телефон")
                    email = input("Email (необязательно): ").strip() or None

                    try:
                        cid = add_contact(name, phone, email)
                        print(f"Контакт добавлен с ID = {cid}")
                    except ValueError as e:
                        print("Ошибка:", e)

                elif choice == "2":
                    get_contacts()

                elif choice == "3":
                    cid = input("Введите ID контакта: ").strip()
                    if not cid.isdigit():
                        print("Неверный ID")
                        continue
                    rec = get_contact_by_id(int(cid))
                    if not rec:
                        print("Контакт не найден")
                    else:
                        id_, name, phone, email = rec
                        print(f"\nID: {id_}\nИмя: {name}\nТелефон: {phone}\nEmail: {email or ''}\n")

                elif choice == "4":
                    cid = input("Введите ID для редактирования: ").strip()
                    if not cid.isdigit():
                        print("Неверный ID")
                        continue
                    rec = get_contact_by_id(int(cid))
                    if not rec:
                        print("Контакт не найден")
                        continue
                    id_, name, phone, email = rec
                    print("Оставьте поле пустым, чтобы оставить текущее значение")
                    new_name = input(f"Имя [{name}]: ").strip() or name
                    new_phone = input(f"Телефон [{phone}]: ").strip() or phone
                    new_email = input(f"Email [{email or ''}]: ").strip() or email
                    try:
                        update_contact(id_, new_name, new_phone, new_email)
                        print("Контакт обновлён")
                    except ValueError as e:
                        print("Ошибка:", e)

                elif choice == "5":
                    cid = input("Введите ID для удаления: ").strip()
                    if not cid.isdigit():
                        print("Неверный ID")
                        continue
                    rec = get_contact_by_id(int(cid))
                    if not rec:
                        print("Контакт не найден")
                        continue
                    confirm = input(f"Удалить контакт {rec[1]} (ID={rec[0]})? (y/N): ").strip().lower()
                    if confirm == "y":
                        delete_contact(int(cid))
                        print("Контакт удалён")
                    else:
                        print("Отмена")

                elif choice == "6":
                    path = input("Путь для JSON (по умолчанию phonebook_export.json): ").strip() or "phonebook_export.json"
                    export_json(path)

                elif choice == "7":
                    path = input("Путь для CSV (по умолчанию phonebook_export.csv): ").strip() or "phonebook_export.csv"
                    export_csv(path)

                elif choice == "8":
                    path = input("Путь JSON для импорта: ").strip()
                    if path == "":
                        print("Путь не указан")
                    else:
                        import_json(path)

                elif choice == "9":
                    path = input("Путь CSV для импорта: ").strip()
                    if path == "":
                        print("Путь не указан")
                    else:
                        import_csv(path)

                elif choice == "0":
                    print("Выход...")
                    break

                else:
                    print("Неправильный пункт меню. Попробуйте ещё раз")
            except Exception as e:
                print("Произошла ошибка:", e)
    except KeyboardInterrupt:
        print("\nПрограмма завершена корректно")


if __name__ == "__main__":
    main()
