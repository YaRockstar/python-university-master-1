from abc import ABC, abstractmethod
from typing import Optional

from domain.vehicle import Vehicle


class MaintenanceRequest:
    """Класс для представления запроса на техническое обслуживание."""

    def __init__(self, vehicle: Vehicle, cost: float, description: str) -> None:
        """Инициализация запроса на техническое обслуживание."""
        self.vehicle = vehicle
        self.cost = cost
        self.description = description


class Handler(ABC):
    """Базовый класс для обработчиков в цепочке обязанностей."""

    def __init__(self, next_handler: Optional["Handler"] = None) -> None:
        """Инициализация обработчика."""
        self._next = next_handler

    def set_next(self, next_handler: "Handler") -> "Handler":
        """Установка следующего обработчика в цепочке."""
        self._next = next_handler
        return next_handler

    def handle(self, request: MaintenanceRequest) -> str:
        """Обработка запроса на обслуживание."""
        res = self._handle(request)

        if res:
            return res

        if self._next:
            return self._next.handle(request)

        return "Запрос не обработан."

    @abstractmethod
    def _handle(self, request: MaintenanceRequest) -> Optional[str]:
        """Обработка запроса (реализуется в подклассах)."""
        pass


class Mechanic(Handler):
    """Обработчик запросов на обслуживание: механик (до 500 у.е.)."""

    def _handle(self, request: MaintenanceRequest) -> Optional[str]:
        """Обработка запроса на обслуживание стоимостью до 500 у.е."""
        if request.cost <= 500:
            return f"Механик одобрил обслуживание: {request.description} ({request.cost} у.е.)"

        return None


class DepartmentHead(Handler):
    """Обработчик запросов на обслуживание: руководитель отдела (500-5000 у.е.)."""

    def _handle(self, request: MaintenanceRequest) -> Optional[str]:
        """Обработка запроса на обслуживание стоимостью от 500 до 5000 у.е."""
        if 500 < request.cost <= 5000:
            return f"Руководитель отдела одобрил обслуживание: {request.description} ({request.cost} у.е.)"
        
        return None


class Director(Handler):
    """Обработчик запросов на обслуживание: директор (любая стоимость)."""

    def _handle(self, request: MaintenanceRequest) -> Optional[str]:
        """Обработка запроса на обслуживание любой стоимости."""
        if request.cost > 0:
            return f"Директор одобрил обслуживание: {request.description} ({request.cost} у.е.)"

        return None
