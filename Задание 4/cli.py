from typing import Optional

from application.services import TransportCompany
from core.exceptions import (
    InvalidVehicleError,
    PermissionDeniedError,
    DriverNotFoundError,
)
from domain import User, Address, Driver
from infrastructure.config import logger
from infrastructure.factories import VehicleFactory


def _input_nonempty(prompt: str) -> str:
    """Запрос непустой строки у пользователя."""
    while True:
        value = input(prompt).strip()
        if value:
            return value

        print("Поле не может быть пустым. Повторите ввод.")


def _input_int(prompt: str, min_value: Optional[int] = None) -> int:
    """Запрос целого числа."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if min_value is not None and value < min_value:
                print(f"Число должно быть не меньше {min_value}.")
                continue

            return value
        except ValueError:
            print("Ошибка: введите целое число.")


def _input_float(prompt: str, min_value: Optional[float] = None) -> float:
    """Запрос числа с плавающей точкой."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if min_value is not None and value < min_value:
                print(f"Число должно быть не меньше {min_value}.")
                continue

            return value
        except ValueError:
            print("Ошибка: введите число.")


def select_vehicle_type() -> str:
    """Выбор типа ТС пользователем."""
    print("Выберите тип транспортного средства:")
    print("1) Bus (автобус)")
    print("2) Truck (грузовик)")
    print("3) Taxi (такси)")

    while True:
        choice = input("Ваш выбор (1-3): ").strip()
        if choice == "1":
            return "bus"
        if choice == "2":
            return "truck"
        if choice == "3":
            return "taxi"
        print("Некорректный выбор. Повторите.")


def add_vehicle_cli(company: TransportCompany, user: User) -> None:
    """Добавление ТС через консоль."""
    vehicle_type = select_vehicle_type()
    vehicle_id = _input_nonempty("ID ТС: ")
    model = _input_nonempty("Модель: ")
    year = _input_int("Год выпуска: ", min_value=1900)
    capacity = _input_int("Вместимость (целое число): ", min_value=0)

    extra_kwargs = {}
    if vehicle_type == "bus":
        extra_kwargs["route_number"] = _input_nonempty("Номер маршрута: ")
    elif vehicle_type == "truck":
        extra_kwargs["cargo_capacity"] = _input_float(
            "Грузоподъёмность (тонн): ", min_value=0.0
        )
    elif vehicle_type == "taxi":
        extra_kwargs["license_plate"] = _input_nonempty("Номерной знак: ")

    try:
        vehicle = VehicleFactory.create_vehicle(
            vehicle_type,
            vehicle_id=vehicle_id,
            model=model,
            year=year,
            capacity=capacity,
            **extra_kwargs,
        )
        company.add_vehicle(user=user, vehicle=vehicle)
        print(f"✔ ТС добавлено: {vehicle}")
    except (InvalidVehicleError, PermissionDeniedError) as e:
        print(f"Ошибка при добавлении ТС: {e}")


def add_driver_cli(company: TransportCompany, user: User) -> None:
    """Добавление водителя через консоль."""
    name = _input_nonempty("Имя и фамилия водителя: ")
    driver_id = _input_nonempty("ID водителя: ")
    license_type = _input_nonempty("Тип прав (например, B, C, D): ")

    city = _input_nonempty("Город: ")
    street = _input_nonempty("Улица: ")
    house = _input_nonempty("Дом: ")

    driver = Driver(name, driver_id, license_type, Address(city, street, house))

    try:
        company.add_driver(user=user, driver=driver)
        print(f"Водитель добавлен: {driver.name} (ID={driver.driver_id})")
    except (InvalidVehicleError, PermissionDeniedError) as e:
        print(f"Ошибка при добавлении водителя: {e}")


def assign_driver_cli(company: TransportCompany, user: User) -> None:
    """Назначение водителя на ТС."""
    driver_id = _input_nonempty("ID водителя: ")
    vehicle_id = _input_nonempty("ID ТС: ")
    try:
        company.assign_driver_to_vehicle(user=user, driver_id=driver_id, vehicle_id=vehicle_id)
        print("Водитель успешно назначен на ТС.")
    except (DriverNotFoundError, InvalidVehicleError, PermissionDeniedError) as e:
        print(f"Ошибка при назначении водителя: {e}")


def list_vehicles_cli(company: TransportCompany) -> None:
    """Вывод списка ТС."""
    vehicles = company.get_all_vehicles()
    if not vehicles:
        print("В парке пока нет транспортных средств.")
        return

    print("Транспортные средства в парке:")
    for v in vehicles:
        print(f"- {v.vehicle_id}: {v}")


def list_drivers_cli(company: TransportCompany) -> None:
    """Вывод списка водителей."""
    if not company._drivers:
        print("Водителей пока нет.")
        return

    print("Водители:")
    for d in company._drivers.values():
        assigned = d.get_assigned_vehicle()
        if assigned:
            print(f"- {d.driver_id}: {d.name}, права {d.license_type}, ТС={assigned.vehicle_id}")
        else:
            print(f"- {d.driver_id}: {d.name}, права {d.license_type}, ТС не назначено")


def search_by_model_cli(company: TransportCompany) -> None:
    """Поиск ТС по подстроке модели."""
    q = _input_nonempty("Введите подстроку модели для поиска: ")
    res = company.search_by_model(q)
    if not res:
        print("Ничего не найдено.")
        return

    print(f"Найдено {len(res)} ТС:")
    for v in res:
        print(f"- {v.vehicle_id}: {v}")


def stats_cli(company: TransportCompany) -> None:
    """Показ статистики вместимости по типам."""
    stats = company.stats_capacity_by_type()
    if not stats:
        print("Парк пуст, статистика недоступна.")
        return

    print("Суммарная вместимость по типам ТС:")
    for t, cap in stats.items():
        print(f"- {t}: {cap}")


def save_company_cli(company: TransportCompany) -> None:
    """Сохранение данных компании."""
    company.save()
    print("Данные компании сохранены в data/transport_company.json")


def load_or_create_company() -> TransportCompany:
    """Попытка загрузки компанию, в противном случае создание новой."""
    try:
        company = TransportCompany.load()
        logger.info("Компания загружена из файла.")
        print("Компания загружена из data/transport_company.json.")
        return company
    except FileNotFoundError:
        logger.info("Файл данных не найден, создаётся новая компания.")
        print("Файл данных не найден, создаётся новая компания.")
        return TransportCompany("TransCo")


def print_menu() -> None:
    """Вывод главного меню."""
    print("\n=== Меню системы управления транспортной компанией ===")
    print("1) Показать все транспортные средства")
    print("2) Показать всех водителей")
    print("3) Добавить транспортное средство")
    print("4) Добавить водителя")
    print("5) Назначить водителя на транспортное средство")
    print("6) Поиск ТС по модели")
    print("7) Статистика вместимости по типам")
    print("8) Сохранить данные")
    print("9) Выход")


def main() -> None:
    """Интерактивный CLI для работы с системой."""
    company = load_or_create_company()
    # Упрощение: один пользователь-админ для всех действий.
    current_user = User("cli_admin", ["admin"])

    while True:
        print_menu()
        choice = input("Выберите пункт меню (1-9): ").strip()

        if choice == "1":
            list_vehicles_cli(company)
        elif choice == "2":
            list_drivers_cli(company)
        elif choice == "3":
            add_vehicle_cli(company, current_user)
        elif choice == "4":
            add_driver_cli(company, current_user)
        elif choice == "5":
            assign_driver_cli(company, current_user)
        elif choice == "6":
            search_by_model_cli(company)
        elif choice == "7":
            stats_cli(company)
        elif choice == "8":
            save_company_cli(company)
        elif choice == "9":
            print("Выход из программы.")
            break
        else:
            print("Некорректный пункт меню, попробуйте ещё раз.")


if __name__ == "__main__":
    main()
