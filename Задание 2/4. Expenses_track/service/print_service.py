from service import expense_service
from service import menu_service
from utils import errors as errors


def show_expenses(expenses):
    """Вывод списка расходов в консоль"""
    if not expenses:
        print(errors.EXPENSES_NOT_FOUND_ERROR)
        return

    print(f"\n{'ID':<4} {'Сумма':<15} {'Дата':<20} {'Категория':<20} {'Описание'}")
    print("-" * 100)

    for expense in expenses:
        expense_id, amount, date, category, description = expense
        print(f"{expense_id:<4} {amount:<15} {date:<20} {category:<20} {description or ''}\n")


def show_menu():
    """Вывод главного меню"""
    print(menu_service.MENU_LIST.get("title"))

    menu_number = 1
    for menu_item in menu_service.MENU_LIST.get("menu_list"):
        print(f'{menu_number}. {menu_item}')
        menu_number += 1
