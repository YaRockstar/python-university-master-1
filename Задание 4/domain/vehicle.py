from abc import ABC, abstractmethod
from typing import Dict, Any

from core.exceptions import InvalidVehicleError
from core.interfaces import Trackable, Reportable
from core.meta import VehicleMeta
from core.mixins import LoggingMixin, NotificationMixin


class Vehicle(LoggingMixin, NotificationMixin, ABC, metaclass=VehicleMeta):
    """Базовый класс транспортного средства. """

    def __init__(self, vehicle_id: str, model: str, year: int, capacity: int, status: str = "idle") -> None:
        """Инициализация транспортного средства."""
        self.__vehicle_id = vehicle_id
        self.__model = model
        self.__year = year
        self.__capacity = capacity
        self.__status = status
        self._last_location = "N/A"
        if self.__year < 1900 or self.__capacity < 0:
            raise InvalidVehicleError("Некорректные год выпуска или вместимость.")

    @property
    def vehicle_id(self) -> str:
        """Возвращение идентификатора транспортного средства."""
        return self.__vehicle_id

    @vehicle_id.setter
    def vehicle_id(self, value: str) -> None:
        """Установка идентификатора транспортного средства."""
        if not value:
            raise InvalidVehicleError("Пустой идентификатор ТС.")
        self.__vehicle_id = value

    @property
    def model(self) -> str:
        """Возвращение модели транспортного средства."""
        return self.__model

    @model.setter
    def model(self, value: str) -> None:
        """Установка модели транспортного средства."""
        if not value:
            raise InvalidVehicleError("Пустая модель ТС.")
        self.__model = value

    @property
    def year(self) -> int:
        """Возвращение года выпуска транспортного средства."""
        return self.__year

    @year.setter
    def year(self, value: int) -> None:
        """Установка года выпуска транспортного средства."""
        if value < 1900:
            raise InvalidVehicleError("Слишком ранний год выпуска.")
        self.__year = value

    @property
    def capacity(self) -> int:
        """Возвращение вместимости транспортного средства."""
        return self.__capacity

    @capacity.setter
    def capacity(self, value: int) -> None:
        """Установка вместимости транспортного средства."""
        if value < 0:
            raise InvalidVehicleError("Отрицательная вместимость.")
        self.__capacity = value

    @property
    def status(self) -> str:
        """Возвращение статуса транспортного средства."""
        return self.__status

    @status.setter
    def status(self, value: str) -> None:
        """Установка статуса транспортного средства."""
        if value not in {"idle", "on_route", "maintenance", "retired"}:
            raise InvalidVehicleError("Недопустимый статус ТС.")
        self.__status = value

    def __eq__(self, other: Any) -> Any:
        """Сравнение двух транспортных средств на равенство."""
        if not isinstance(other, Vehicle):
            return NotImplemented

        return (self.year, self.capacity, self.model) == (other.year, other.capacity, other.model)

    def __lt__(self, other: Any) -> bool:
        """Сравнение транспортных средств по году выпуска и вместимости."""
        if not isinstance(other, Vehicle):
            return NotImplemented

        return (self.year, self.capacity) < (other.year, other.capacity)

    def __gt__(self, other: Any) -> bool:
        """Сравнение транспортных средств по году выпуска и вместимости."""
        if not isinstance(other, Vehicle):
            return NotImplemented

        return (self.year, self.capacity) > (other.year, other.capacity)

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование транспортного средства в словарь для сериализации."""
        return {
            "type": self.__class__.__name__.lower(),
            "vehicle_id": self.vehicle_id,
            "model": self.model,
            "year": self.year,
            "capacity": self.capacity,
            "status": self.status,
            **self._extra_dict()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Vehicle":
        """Создание транспортного средства из словаря."""
        from core.meta import VehicleMeta

        vehicle_type = data.get("type")
        klass = VehicleMeta.registry.get(vehicle_type)

        if not klass:
            raise InvalidVehicleError(f"Неизвестный тип ТС: {vehicle_type}")

        return klass._from_dict_impl(data)

    @abstractmethod
    def calculate_cost(self, distance_km: float) -> float:
        """Расчёт стоимости эксплуатации транспортного средства."""
        pass

    def _extra_dict(self) -> Dict[str, Any]:
        """Возвращение дополнительных данных для сериализации подклассов."""
        return {}

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> "Vehicle":
        """Реализация создания экземпляра из словаря для конкретного подкласса."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Возвращение строкового представления транспортного средства."""
        return f"Транспортное средство: {self.model}, Год выпуска: {self.year}"


class Bus(Vehicle):
    """Автобус — транспортное средство с номером маршрута."""

    def __init__(self, vehicle_id: str, model: str, year: int, capacity: int, route_number: str,
                 status: str = "idle") -> None:
        """Инициализация автобуса."""
        super().__init__(vehicle_id, model, year, capacity, status)
        self.__route_number = route_number

    @property
    def route_number(self) -> str:
        """Возвращение номера маршрута автобуса."""
        return self.__route_number

    @route_number.setter
    def route_number(self, value: str) -> None:
        """Установка номера маршрута автобуса."""
        if not value:
            raise InvalidVehicleError("Пустой номер маршрута.")
        self.__route_number = value

    def calculate_cost(self, distance_km: float) -> float:
        """Расчёт стоимости эксплуатации автобуса."""
        return round(1.2 * distance_km + 0.05 * self.capacity, 2)

    def __str__(self) -> str:
        """Возвращение строкового представления автобуса."""
        return f"Автобус: {self.model}, Маршрут: {self.route_number}, Год: {self.year}"

    def _extra_dict(self) -> Dict[str, Any]:
        """Возвращение дополнительных данных автобуса для сериализации."""
        return {"route_number": self.route_number}

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> "Bus":
        """Создание автобуса из словаря."""
        return cls(
            vehicle_id=data["vehicle_id"],
            model=data["model"],
            year=int(data["year"]),
            capacity=int(data["capacity"]),
            route_number=data.get("route_number", ""),
            status=data.get("status", "idle"),
        )


class Truck(Vehicle):
    """Грузовик — транспортное средство с грузоподъёмностью."""

    def __init__(self, vehicle_id: str, model: str, year: int, capacity: int, cargo_capacity: float,
                 status: str = "idle") -> None:
        """Инициализация грузовика."""
        super().__init__(vehicle_id, model, year, capacity, status)
        if cargo_capacity < 0:
            raise InvalidVehicleError("Отрицательная грузоподъёмность.")
        self.__cargo_capacity = cargo_capacity  # тонны

    @property
    def cargo_capacity(self) -> float:
        """Возвращение грузоподъёмности грузовика в тоннах."""
        return self.__cargo_capacity

    @cargo_capacity.setter
    def cargo_capacity(self, value: float) -> None:
        """Установка грузоподъёмности грузовика."""
        if value < 0:
            raise InvalidVehicleError("Отрицательная грузоподъёмность.")
        self.__cargo_capacity = value

    def calculate_cost(self, distance_km: float) -> float:
        """Расчёт стоимости эксплуатации грузовика."""
        return round(2.0 * distance_km + 10.0 * self.cargo_capacity, 2)

    def __str__(self) -> str:
        """Возвращение строкового представления грузовика."""
        return f"Грузовик: {self.model}, Г/п: {self.cargo_capacity}т, Год: {self.year}"

    def _extra_dict(self) -> Dict[str, Any]:
        """Возвращение дополнительных данных грузовика для сериализации."""
        return {"cargo_capacity": self.cargo_capacity}

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> "Truck":
        """Создание грузовика из словаря."""
        return cls(
            vehicle_id=data["vehicle_id"],
            model=data["model"],
            year=int(data["year"]),
            capacity=int(data["capacity"]),
            cargo_capacity=float(data.get("cargo_capacity", 0)),
            status=data.get("status", "idle"),
        )


class Taxi(Vehicle):
    """Такси — транспортное средство с номерным знаком."""

    def __init__(self, vehicle_id: str, model: str, year: int, capacity: int, license_plate: str,
                 status: str = "idle") -> None:
        """Инициализация такси."""
        super().__init__(vehicle_id, model, year, capacity, status)
        self.__license_plate = license_plate

    @property
    def license_plate(self) -> str:
        """Возвращение номерного знака такси."""
        return self.__license_plate

    @license_plate.setter
    def license_plate(self, value: str) -> None:
        """Установка номерного знака такси."""
        if not value:
            raise InvalidVehicleError("Пустой номерной знак.")
        self.__license_plate = value

    def calculate_cost(self, distance_km: float) -> float:
        """Расчёт стоимости эксплуатации такси."""
        base = 3.0
        return round(base + 0.8 * distance_km, 2)

    def __str__(self) -> str:
        """Возвращение строкового представления такси."""
        return f"Такси: {self.model}, Номер: {self.license_plate}, Год: {self.year}"

    def _extra_dict(self) -> Dict[str, Any]:
        """Возвращение дополнительных данных такси для сериализации."""
        return {"license_plate": self.license_plate}

    @classmethod
    def _from_dict_impl(cls, data: Dict[str, Any]) -> "Taxi":
        """Создание такси из словаря."""
        return cls(
            vehicle_id=data["vehicle_id"],
            model=data["model"],
            year=int(data["year"]),
            capacity=int(data["capacity"]),
            license_plate=data.get("license_plate", ""),
            status=data.get("status", "idle"),
        )


class TrackableBus(Bus, Trackable):
    """Автобус с возможностью отслеживания местоположения."""

    def track_location(self) -> str:
        """Возвращение информации о текущем местоположении автобуса."""
        return f"Автобус {self.model} на маршруте {self.route_number} — позиция: {self._last_location}"

    def update_location(self, location: str) -> None:
        """Обновление местоположения автобуса."""
        self._last_location = location


class ReportableTaxi(Taxi, Reportable):
    """Такси с возможностью генерации отчётов по рейсам."""

    def generate_report(self) -> str:
        """Генерация отчёта по рейсу такси."""
        return f"Отчёт по рейсу такси {self.license_plate}: статус={self.status}, последняя позиция={self._last_location}"

    def update_location(self, location: str) -> None:
        """Обновление местоположения такси."""
        self._last_location = location
