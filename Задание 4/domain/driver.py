from typing import Optional, Dict, Any

from domain.address import Address
from domain.vehicle import Vehicle


class Driver:
    """Класс для представления водителя транспортной компании."""

    def __init__(self, name: str, driver_id: str, license_type: str, address: Address,
                 assigned_vehicle: Optional[Vehicle] = None) -> None:
        """Инициализация водителя."""
        self.name = name
        self.driver_id = driver_id
        self.license_type = license_type
        self.address = address
        self._assigned_vehicle = assigned_vehicle

    def assign_vehicle(self, vehicle: Vehicle) -> None:
        """Закрепление транспортного средства за водителем."""
        self._assigned_vehicle = vehicle

    def remove_vehicle(self) -> None:
        """Открепление транспортного средства от водителя."""
        self._assigned_vehicle = None

    def get_assigned_vehicle(self) -> Optional[Vehicle]:
        """Возвращение закреплённого транспортного средства."""
        return self._assigned_vehicle

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование водителя в словарь для сериализации."""
        return {
            "name": self.name,
            "driver_id": self.driver_id,
            "license_type": self.license_type,
            "address": self.address.to_dict(),
            "assigned_vehicle": self._assigned_vehicle.to_dict() if self._assigned_vehicle else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Driver":
        """Создание водителя из словаря."""
        from domain.vehicle import Vehicle
        addr = Address.from_dict(data["address"])
        veh = Vehicle.from_dict(data["assigned_vehicle"]) if data.get("assigned_vehicle") else None
        return cls(
            name=data["name"],
            driver_id=data["driver_id"],
            license_type=data["license_type"],
            address=addr,
            assigned_vehicle=veh
        )
