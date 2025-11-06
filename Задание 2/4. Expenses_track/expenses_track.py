from config import db_config as config
from service import expense_service
from service import export_service
from service import print_service
from utils import errors
from utils import helper
from utils import validator


def main():
    try:
        config.init_db()
        while True:
            print_service.show_menu()
            choice = helper.prompt("\nВыберите пункт: ")

            try:
                if choice == "1":
                    amount = helper.prompt("Сумма: ")
                    expense_date = validator.validate_date(helper.prompt("Дата: "))
                    category = helper.prompt("Категория: ").lower()
                    description = helper.prompt("Описание (необязательно): ", None)

                    try:
                        expense_id = expense_service.add_expense(amount, expense_date, category, description)
                        print(f"Расход добавлен с ID = {expense_id}")
                    except ValueError as e:
                        print(errors.BASE_ERROR, e)

                elif choice == "2":
                    expenses = expense_service.get_all_expenses()
                    print_service.show_expenses(expenses)

                elif choice == "3":
                    category = helper.prompt("Категория: ").lower()
                    expenses = expense_service.get_expenses_by_category(category)
                    print_service.show_expenses(expenses)

                elif choice == "4":
                    date = validator.validate_date(helper.prompt("Дата: "))
                    expenses = expense_service.get_expenses_by_date(date)
                    print_service.show_expenses(expenses)

                elif choice == "5":
                    expense_id = helper.prompt("Введите ID расхода: ")
                    if not expense_id.isdigit():
                        print(errors.INCORRECT_ID_ERROR)
                        continue

                    expense = expense_service.get_expense_by_id(int(expense_id))
                    if not expense:
                        print(errors.EXPENSES_NOT_FOUND_ERROR)
                    else:
                        expense_id, amount, date, category, description = expense
                        print(f"{expense_id:<4} {amount:<15} {date:<20} {category:<10} {description or ''}\n")

                elif choice == "6":
                    path = helper.prompt(
                        "Путь для CSV (по умолчанию expenses_export.csv): ",
                        "expenses_export.csv"
                    )
                    export_service.export_expenses_to_csv(path)

                elif choice == "7":
                    print("Выход")
                    break

                else:
                    print(errors.INCORRECT_MENU_ERROR)
            except Exception as e:
                print(errors.BASE_ERROR, e)
    except KeyboardInterrupt:
        print("\nПрограмма завершена корректно")
    except Exception as e:
        print(errors.BASE_ERROR, e)


if __name__ == "__main__":
    main()
