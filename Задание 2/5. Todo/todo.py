import sqlite3
from datetime import datetime

DB_NAME = "tasks.db"


def get_connection():
    """Предоставление коннекшена к БД"""
    return sqlite3.connect(DB_NAME)


def init_db():
    """Инициализация БД"""
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                created_at TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
            )
        """)
        connection.commit()


def add_task(description):
    """Добавление задачи"""
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as connection:
        connection.execute(
            "INSERT INTO tasks (description, created_at, done) VALUES (?, ?, ?)",
            (description, created_at, 0),
        )
        connection.commit()


def mark_done(task_id: int):
    """Отметка задачи"""
    with get_connection() as connection:
        cur = connection.execute(
            "UPDATE tasks SET done = 1 WHERE id = ?",
            (task_id,)
        )
        if cur.rowcount == 0:
            raise ValueError("Задача с таким ID не найдена")
        connection.commit()


def delete_task(task_id: int):
    """Удаление задачи"""
    with get_connection() as connection:
        cur = connection.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )
        if cur.rowcount == 0:
            raise ValueError("Задача с таким ID не найдена")
        connection.commit()


def get_all_tasks():
    """Получение всех задач"""
    with get_connection() as connection:
        return connection.execute(
            "SELECT id, description, created_at, done FROM tasks ORDER BY id DESC"
        ).fetchall()


def print_tasks(tasks):
    """Вывод задач"""
    if not tasks:
        print("Список задач пуст.")
        return

    print("\nСписок задач:")
    print("=" * 50)
    for task in tasks:
        task_id, desc, created, done = task
        status = "[x]" if done else "[ ]"
        print(f"{task_id:<3} {status} {desc} (создана {created})")
    print()


def show_menu():
    """Вывод меню"""
    print("""
===== Менеджер задач =====
1. Добавить задачу
2. Отметить задачу как выполненную
3. Удалить задачу
4. Показать все задачи
5. Выход
    """)


def main():
    init_db()

    try:
        while True:
            show_menu()
            choice = input("Выберите пункт: ").strip()

            if choice == "1":
                desc = input("Введите описание задачи: ").strip()
                if desc:
                    add_task(desc)
                    print("Задача добавлена")
                else:
                    print("Описание не может быть пустым")

            elif choice == "2":
                task_id = int(input("Введите ID задачи для отметки: ").strip())
                mark_done(task_id)
                print("Задача отмечена как выполненная")

            elif choice == "3":
                task_id = int(input("Введите ID задачи для удаления: ").strip())
                delete_task(task_id)
                print("Задача удалена")

            elif choice == "4":
                tasks = get_all_tasks()
                print_tasks(tasks)

            elif choice == "5":
                print("Выход")
                break

            else:
                print("Неверный пункт меню")
    except KeyboardInterrupt:
        print("\nПрограмма завершена корректно")


if __name__ == "__main__":
    main()
