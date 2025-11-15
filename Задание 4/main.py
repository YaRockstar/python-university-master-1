from application.patterns import Mechanic, DepartmentHead, Director, MaintenanceRequest, BusCostCalculator, \
    TruckCostCalculator
from application.services import TransportCompany
from domain import TrackableBus
from domain import User, Address, Driver, ReportableTaxi
from infrastructure.config import logger
from infrastructure.factories import VehicleFactory


def main():
    admin = User("alice", ["admin"])
    dispatcher = User("bob", ["dispatcher"])

    company = TransportCompany("TransCo")
    bus = VehicleFactory.create_vehicle("bus", vehicle_id="B-1", model="LiAZ-5292", year=2020, capacity=110,
                                        route_number="42")
    truck = VehicleFactory.create_vehicle("truck", vehicle_id="T-1", model="Volvo FH", year=2018, capacity=2,
                                          cargo_capacity=20.0)
    taxi = ReportableTaxi(vehicle_id="TX-7", model="Skoda Octavia", year=2022, capacity=4, license_plate="ABC-777")

    company.add_vehicle(user=admin, vehicle=bus)
    company.add_vehicle(user=dispatcher, vehicle=truck)
    company.add_vehicle(user=admin, vehicle=taxi)

    d1 = Driver("Иван Петров", "D001", "D", Address("Казань", "Ленина", "10"))
    d2 = Driver("Павел Сидоров", "D002", "C+E", Address("Казань", "Кремлёвская", "1"))
    company.add_driver(user=dispatcher, driver=d1)
    company.add_driver(user=admin, driver=d2)
    company.assign_driver_to_vehicle(user=dispatcher, driver_id="D001", vehicle_id="B-1")

    found = company.search_by_model("volvo")
    logger.info(f"Найдено по модели 'volvo': {len(found)} шт. -> {[str(v) for v in found]}")
    logger.info(f"Суммарная вместимость по типам: {company.stats_capacity_by_type()}")

    bus_calc = BusCostCalculator()
    truck_calc = TruckCostCalculator()
    logger.info(f"Bus TM calc: {bus_calc.calculate_cost(bus, 25)} у.е.")
    logger.info(f"Truck TM calc: {truck_calc.calculate_cost(truck, 200)} у.е.")

    logger.info(f"Bus.calculate_cost(25): {bus.calculate_cost(25)} у.е.")
    logger.info(f"Truck.calculate_cost(200): {truck.calculate_cost(200)} у.е.")
    logger.info(f"Taxi.calculate_cost(12.5): {taxi.calculate_cost(12.5)} у.е.")

    tb = TrackableBus("B-2", "MAZ-203", 2019, 100, "7")
    tb.update_location("N55.79 E49.11")
    logger.info(tb.track_location())

    taxi.update_location("N55.79 E49.12")
    logger.info(taxi.generate_report())

    chain = Mechanic()
    chain.set_next(DepartmentHead()).set_next(Director())
    req_small = MaintenanceRequest(bus, 300, "Замена ламп и мелкий ремонт салона")
    req_mid = MaintenanceRequest(truck, 1500, "Замена тормозных колодок")
    req_big = MaintenanceRequest(taxi, 10000, "Капитальный ремонт двигателя")
    for r in (req_small, req_mid, req_big):
        logger.info(chain.handle(r))

    company.save()
    logger.info("Данные сохранены в data/transport_company.json")


if __name__ == "__main__":
    main()
