from abc import ABC, abstractmethod


class Trackable(ABC):
    """Интерфейс отслеживания местоположения транспортного средства."""

    @abstractmethod
    def track_location(self) -> str:
        """Возврат строки с информацией о текущем местоположении ТС."""
        pass


class Reportable(ABC):
    """Интерфейс генерации отчётов по рейсам/поездкам."""

    @abstractmethod
    def generate_report(self) -> str:
        """Возврат строки с отчётом по рейсу."""
        pass
