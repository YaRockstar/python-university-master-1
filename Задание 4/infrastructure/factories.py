from typing import Any

from core.exceptions import InvalidVehicleError
from core.meta import VehicleMeta
from domain.vehicle import Vehicle


class VehicleFactory:
    """Фабричный метод создания транспортного средства по строковому типу и параметрам."""

    @staticmethod
    def create_vehicle(vehicle_type: str, **kwargs: Any) -> Vehicle:
        """Создание транспортного средства указанного типа."""
        klass = VehicleMeta.registry.get(vehicle_type.lower())
        if not klass:
            raise InvalidVehicleError(f"Неизвестный тип транспортного средства: {vehicle_type}")

        return klass(**kwargs)
