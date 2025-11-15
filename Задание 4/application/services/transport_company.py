import json
import os
from typing import Dict, List, Optional

from core.exceptions import InvalidVehicleError, DriverNotFoundError
from domain.driver import Driver
from domain.vehicle import Vehicle
from utils.decorators import check_permissions

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)


class TransportCompany:
    """Фасад над коллекциями ТС и водителей. Поддержка CRUD, поиск, анализ и сериализации."""

    def __init__(self, name: str) -> None:
        """Инициализация транспортной компании."""
        self.name = name
        self._vehicles: Dict[str, Vehicle] = {}
        self._drivers: Dict[str, Driver] = {}

    @check_permissions(["admin", "manager", "dispatcher"])
    def add_vehicle(self, user, vehicle: Vehicle) -> None:
        """Добавление транспортного средства в парк компании."""
        if vehicle.vehicle_id in self._vehicles:
            raise InvalidVehicleError("ТС с таким идентификатором уже существует.")

        self._vehicles[vehicle.vehicle_id] = vehicle
        vehicle.log_action(f"Добавлено ТС {vehicle}")

    @check_permissions(["admin", "manager"])
    def remove_vehicle(self, user, vehicle_id: str) -> None:
        """Удаление транспортного средства из парка компании."""
        self._vehicles.pop(vehicle_id, None)

    def get_all_vehicles(self) -> List[Vehicle]:
        """Возврат списка всех транспортных средств компании."""
        return list(self._vehicles.values())

    def search_by_model(self, model_substr: str) -> List[Vehicle]:
        """Поиск транспортных средств по подстроке в названии модели."""
        q = model_substr.lower()
        return [v for v in self._vehicles.values() if q in v.model.lower()]

    @check_permissions(["admin", "manager", "dispatcher"])
    def add_driver(self, user, driver: Driver) -> None:
        """Добавление водителя в компанию."""
        if driver.driver_id in self._drivers:
            raise InvalidVehicleError("Водитель с таким id уже существует.")

        self._drivers[driver.driver_id] = driver

    @check_permissions(["admin", "manager"])
    def remove_driver(self, user, driver_id: str) -> None:
        """Удаление водителя из компании."""
        self._drivers.pop(driver_id, None)

    def get_driver(self, driver_id: str) -> Driver:
        """Возврат водителя по идентификатору."""
        d = self._drivers.get(driver_id)
        if not d:
            raise DriverNotFoundError("Водитель не найден.")
        return d

    @check_permissions(["admin", "manager", "dispatcher"])
    def assign_driver_to_vehicle(self, user, driver_id: str, vehicle_id: str) -> None:
        """Назначение водителя на транспортное средство."""
        d = self.get_driver(driver_id)
        v = self._vehicles.get(vehicle_id)

        if not v:
            raise InvalidVehicleError("ТС не найдено.")

        d.assign_vehicle(v)
        v.log_action(f"Водитель {d.name} назначен на {v}")

    def save(self, path: Optional[str] = None) -> None:
        """Сохранение данных компании в JSON-файл."""
        if path is None:
            path = os.path.join(DATA_DIR, "transport_company.json")
        else:
            # Добавление директории data, если путь относительный и не содержит её.
            if not os.path.isabs(path) and DATA_DIR not in path:
                path = os.path.join(DATA_DIR, os.path.basename(path))

        data = {
            "name": self.name,
            "vehicles": [v.to_dict() for v in self._vehicles.values()],
            "drivers": [d.to_dict() for d in self._drivers.values()],
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path: Optional[str] = None) -> "TransportCompany":
        """Загрузка данные компании из JSON-файла."""
        if path is None:
            path = os.path.join(DATA_DIR, "transport_company.json")
        else:
            # Добавление директории data, если путь относительный и не содержит её.
            if not os.path.isabs(path) and DATA_DIR not in path:
                path = os.path.join(DATA_DIR, os.path.basename(path))

        from domain.vehicle import Vehicle
        from domain.driver import Driver

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        comp = cls(data["name"])

        for vdata in data["vehicles"]:
            v = Vehicle.from_dict(vdata)
            comp._vehicles[v.vehicle_id] = v

        for ddata in data["drivers"]:
            d = Driver.from_dict(ddata)
            comp._drivers[d.driver_id] = d

        return comp

    def stats_capacity_by_type(self) -> Dict[str, int]:
        """Возврат статистики суммарной вместимости по типам транспортных средств."""
        res: Dict[str, int] = {}

        for v in self._vehicles.values():
            t = v.__class__.__name__
            res[t] = res.get(t, 0) + v.capacity

        return res
