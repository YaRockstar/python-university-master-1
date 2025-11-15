from application.patterns import (
    Mechanic,
    DepartmentHead,
    Director,
    MaintenanceRequest,
    BusCostCalculator,
    TruckCostCalculator,
)
from application.services import TransportCompany
from core.exceptions import (
    InvalidVehicleError,
    PermissionDeniedError,
    DriverNotFoundError,
)
from domain import TrackableBus
from domain import User, Address, Driver, ReportableTaxi
from infrastructure.config import logger
from infrastructure.factories import VehicleFactory


def setup_company():
    """Создание компании, пользователей, транспорта и водителей, выполнение базовой настройки."""
    admin = User("alice", ["admin"])
    dispatcher = User("bob", ["dispatcher"])

    company = TransportCompany("TransCo")

    bus = VehicleFactory.create_vehicle(
        "bus",
        vehicle_id="B-1",
        model="LiAZ-5292",
        year=2020,
        capacity=110,
        route_number="42",
    )
    truck = VehicleFactory.create_vehicle(
        "truck",
        vehicle_id="T-1",
        model="Volvo FH",
        year=2018,
        capacity=2,
        cargo_capacity=20.0,
    )
    taxi = ReportableTaxi(
        vehicle_id="TX-7",
        model="Skoda Octavia",
        year=2022,
        capacity=4,
        license_plate="ABC-777",
    )

    company.add_vehicle(user=admin, vehicle=bus)
    company.add_vehicle(user=dispatcher, vehicle=truck)
    company.add_vehicle(user=admin, vehicle=taxi)

    d1 = Driver("Иван Петров", "D001", "D", Address("Казань", "Ленина", "10"))
    d2 = Driver("Павел Сидоров", "D002", "C+E", Address("Казань", "Кремлёвская", "1"))
    company.add_driver(user=dispatcher, driver=d1)
    company.add_driver(user=admin, driver=d2)
    company.assign_driver_to_vehicle(user=dispatcher, driver_id="D001", vehicle_id="B-1")

    return company, admin, dispatcher, bus, truck, taxi


def demo_search_and_stats(company: TransportCompany) -> None:
    """Демонстрация поиска и простой аналитики по парку."""
    logger.info("=== Поиск и аналитика по парку ===")
    found = company.search_by_model("volvo")
    logger.info(
        f"Найдено по модели 'volvo': {len(found)} шт. -> {[str(v) for v in found]}"
    )
    logger.info(
        f"Суммарная вместимость по типам: {company.stats_capacity_by_type()}"
    )


def demo_cost_calculation(bus, truck, taxi) -> None:
    """Демонстрация шаблонного метода и расчёта стоимости в самих ТС."""
    bus_calc = BusCostCalculator()
    truck_calc = TruckCostCalculator()

    logger.info("=== Шаблонный метод (CostCalculator) ===")
    logger.info(f"Bus TM calc (25 км): {bus_calc.calculate_cost(bus, 25)} у.е.")
    logger.info(f"Truck TM calc (200 км): {truck_calc.calculate_cost(truck, 200)} у.е.")

    logger.info("=== calculate_cost в самих транспортных средствах ===")
    logger.info(f"Bus.calculate_cost(25): {bus.calculate_cost(25)} у.е.")
    logger.info(f"Truck.calculate_cost(200): {truck.calculate_cost(200)} у.е.")
    logger.info(f"Taxi.calculate_cost(12.5): {taxi.calculate_cost(12.5)} у.е.")


def demo_tracking_and_reports(taxi: ReportableTaxi) -> None:
    """Демонстрация интерфейсов Trackable и Reportable."""
    logger.info("=== Интерфейсы Trackable / Reportable ===")
    tb = TrackableBus("B-2", "MAZ-203", 2019, 100, "7")
    tb.update_location("N55.79 E49.11")
    logger.info(tb.track_location())

    taxi.update_location("N55.79 E49.12")
    logger.info(taxi.generate_report())


def demo_maintenance_chain(bus, truck, taxi) -> None:
    """Демонстрация цепочки обязанностей для обслуживания ТС."""
    logger.info("=== Цепочка обязанностей для обслуживания ===")
    chain = Mechanic()
    chain.set_next(DepartmentHead()).set_next(Director())

    req_small = MaintenanceRequest(
        bus,
        300,
        "Замена ламп и мелкий ремонт салона",
    )
    req_mid = MaintenanceRequest(
        truck,
        1500,
        "Замена тормозных колодок",
    )
    req_big = MaintenanceRequest(
        taxi,
        10000,
        "Капитальный ремонт двигателя",
    )

    for r in (req_small, req_mid, req_big):
        logger.info(chain.handle(r))


def demo_serialization(company: TransportCompany) -> None:
    """Демонстрация сохранения и загрузки данных компании."""
    logger.info("=== Сериализация и десериализация ===")
    company.save()
    logger.info("Данные сохранены в data/transport_company.json")

    loaded = TransportCompany.load()
    logger.info(
        f"Данные загружены из файла: компания='{loaded.name}', "
        f"количество ТС={len(loaded.get_all_vehicles())}"
    )


def demo_exceptions(company: TransportCompany, admin: User, dispatcher: User) -> None:
    """Демонстрация обработки пользовательских исключений."""
    logger.info("=== Демонстрация обработки пользовательских исключений ===")

    # PermissionDeniedError: попытка выполнить действие без нужной роли.
    try:
        company.remove_vehicle(user=dispatcher, vehicle_id="B-1")
    except PermissionDeniedError as e:
        logger.warning(f"Ожидаемая ошибка прав доступа: {e}")

    # DriverNotFoundError: назначение несуществующего водителя.
    try:
        company.assign_driver_to_vehicle(
            user=admin, driver_id="NO_SUCH", vehicle_id="B-1"
        )
    except DriverNotFoundError as e:
        logger.warning(f"Ожидаемая ошибка поиска водителя: {e}")

    # InvalidVehicleError: попытка создать ТС с некорректными данными.
    try:
        VehicleFactory.create_vehicle(
            "bus",
            vehicle_id="BAD",
            model="OldTimer",
            year=1800,
            capacity=-1,
            route_number="0",
        )
    except InvalidVehicleError as e:
        logger.warning(f"Ожидаемая ошибка валидации ТС: {e}")


def main() -> None:
    """Демонстрационный сценарий работы системы управления транспортной компанией."""
    company, admin, dispatcher, bus, truck, taxi = setup_company()

    demo_search_and_stats(company)
    demo_cost_calculation(bus, truck, taxi)
    demo_tracking_and_reports(taxi)
    demo_maintenance_chain(bus, truck, taxi)
    demo_serialization(company)
    demo_exceptions(company, admin, dispatcher)


if __name__ == "__main__":
    main()
