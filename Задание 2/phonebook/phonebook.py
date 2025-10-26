from config import db_config as config
from services import contact_service
from services import export_service
from services import import_service
from services import print_service
from utils import errors
from utils import helper


def main():
    try:
        config.init_db()
        while True:
            print_service.show_menu()
            choice = helper.prompt("\nВыберите пункт: ")

            try:
                if choice == "1":
                    name = helper.prompt("Имя: ")
                    phone = helper.prompt("Телефон: ")
                    email = helper.prompt("Email (необязательно): ", None)

                    try:
                        contact_id = contact_service.add_contact(name, phone, email)
                        print_service.show_message(f"Контакт добавлен с ID = {contact_id}")
                    except ValueError as e:
                        print_service.show_message(errors.BASE_ERROR, e)

                elif choice == "2":
                    print_service.show_contacts()

                elif choice == "3":
                    contact_id = helper.prompt("Введите ID контакта: ")
                    if not contact_id.isdigit():
                        print_service.show_message(errors.INCORRECT_ID_ERROR)
                        continue

                    contact = contact_service.get_contact_by_id(int(contact_id))
                    if not contact:
                        print_service.show_message(errors.CONTACT_NOT_FOUND_ERROR)
                    else:
                        contact_id, name, phone, email = contact
                        print_service.show_message(
                            f"\nID: {contact_id}\nИмя: {name}\nТелефон: {phone}\nEmail: {email or 'отсутствует'}\n")

                elif choice == "4":
                    contact_id = helper.prompt("Введите ID контакта: ")
                    if not contact_id.isdigit():
                        print_service.show_message(errors.INCORRECT_ID_ERROR)
                        continue

                    contact = contact_service.get_contact_by_id(int(contact_id))
                    if not contact:
                        print_service.show_message(errors.CONTACT_NOT_FOUND_ERROR)
                        continue

                    contact_id, name, phone, email = contact
                    print_service.show_message("Оставьте поле пустым, чтобы оставить текущее значение")

                    new_name = input(f"Имя [{name}]: ").strip() or name
                    new_phone = input(f"Телефон [{phone}]: ").strip() or phone
                    new_email = input(f"Email [{email or ''}]: ").strip() or email

                    try:
                        contact_service.update_contact(contact_id, new_name, new_phone, new_email)
                        print_service.show_message("Контакт обновлён")
                    except ValueError as e:
                        print_service.show_message(errors.BASE_ERROR, e)

                elif choice == "5":
                    contact_id = helper.prompt("Введите ID для удаления: ")
                    if not contact_id.isdigit():
                        print_service.show_message(errors.INCORRECT_ID_ERROR)
                        continue

                    contact = contact_service.get_contact_by_id(int(contact_id))
                    if not contact:
                        print_service.show_message(errors.CONTACT_NOT_FOUND_ERROR)
                        continue

                    confirm = helper.prompt(f"Удалить контакт {contact[1]} (ID={contact[0]})? (y/N): ").lower()
                    if confirm == "y":
                        contact_service.delete_contact(int(contact_id))
                        print_service.show_message("Контакт удалён")
                    else:
                        print_service.show_message("Отмена")

                elif choice == "6":
                    path = helper.prompt(
                        "Путь для JSON (по умолчанию phonebook_export.json): ",
                        "phonebook_export.json"
                    )
                    export_service.export_contacts_to_json(path)

                elif choice == "7":
                    path = helper.prompt(
                        "Путь для CSV (по умолчанию phonebook_export.csv): ",
                        "phonebook_export.csv"
                    )
                    export_service.export_contacts_to_csv(path)

                elif choice == "8":
                    path = helper.prompt("Путь JSON для импорта: ")
                    if path == "":
                        print_service.show_message(errors.PATH_NOT_SPECIFIED_ERROR)
                    else:
                        import_service.import_contacts_from_json(path)

                elif choice == "9":
                    path = helper.prompt("Путь CSV для импорта: ")
                    if path == "":
                        print_service.show_message(errors.PATH_NOT_SPECIFIED_ERROR)
                    else:
                        import_service.import_contacts_from_csv(path)

                elif choice == "10":
                    print_service.show_message("Выход")
                    break

                else:
                    print_service.show_message(errors.INCORRECT_MENU_ERROR)
            except Exception as e:
                print_service.show_message(errors.BASE_ERROR, e)
    except KeyboardInterrupt:
        print_service.show_message("\nПрограмма завершена корректно")
    except Exception as e:
        print_service.show_message(errors.BASE_ERROR, e)


if __name__ == "__main__":
    main()
