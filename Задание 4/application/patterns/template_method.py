from abc import ABC, abstractmethod

from domain.vehicle import Vehicle, Truck


class CostCalculator(ABC):
    """Шаблон расчёта стоимости эксплуатации."""

    def calculate_cost(self, vehicle: Vehicle, distance_km: float) -> float:
        """Расчет стоимости эксплуатации транспортного средства."""
        base = self.get_base_cost(vehicle, distance_km)
        extra = self.get_extra_cost(vehicle, distance_km)
        total = base + extra
        return round(total, 2)

    @abstractmethod
    def get_base_cost(self, vehicle: Vehicle, distance_km: float) -> float:
        """Получение базовой стоимости эксплуатации."""
        pass

    def get_extra_cost(self, vehicle: Vehicle, distance_km: float) -> float:
        """Получение дополнительных расходов на эксплуатацию."""
        return 0.0


class BusCostCalculator(CostCalculator):
    """Калькулятор стоимости эксплуатации автобуса."""

    def get_base_cost(self, vehicle: Vehicle, distance_km: float) -> float:
        """Получение базовой стоимости эксплуатации автобуса."""
        return 1.0 * distance_km

    def get_extra_cost(self, vehicle: Vehicle, distance_km: float) -> float:
        """Получение дополнительных расходов на эксплуатацию автобуса."""
        return 0.05 * vehicle.capacity


class TruckCostCalculator(CostCalculator):
    """Калькулятор стоимости эксплуатации грузовика."""

    def get_base_cost(self, vehicle: Vehicle, distance_km: float) -> float:
        """Получение стоимости эксплуатации грузовика."""
        return 1.6 * distance_km

    def get_extra_cost(self, vehicle: Vehicle, distance_km: float) -> float:
        """Получение дополнительных расходов на эксплуатацию грузовика."""
        cap = vehicle.cargo_capacity if isinstance(vehicle, Truck) else 0.0
        return 8.0 * cap
