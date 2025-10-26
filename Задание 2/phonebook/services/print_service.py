from services import contact_service
from services import menu_service
from utils import errors as errors


def show_message(message, error=''):
    """Вывод сообщения"""
    print(message, error)


def show_contacts():
    """Вывод списка контактов в консоль"""
    contacts = contact_service.get_contacts()

    if not contacts:
        show_message(errors.NO_CONTACTS_ERROR)
        return

    show_message(f"\n{'ID':<4} {'Имя':<30} {'Телефон':<20} {'Email'}")
    show_message("-" * 90)

    for contact in contacts:
        contact_id, name, phone, email = contact
        show_message(f"{contact_id:<4} {name:<30} {phone:<20} {email or ''}\n")


def show_menu():
    """Вывод главного меню"""
    show_message(menu_service.MENU_LIST.get("title"))

    menu_number = 1
    for menu_item in menu_service.MENU_LIST.get("menu_list"):
        show_message(f'{menu_number}. {menu_item}')
        menu_number += 1
