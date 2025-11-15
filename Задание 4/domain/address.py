from typing import Dict


class Address:
    """Класс для представления адреса водителя."""

    def __init__(self, city: str, street: str, house: str) -> None:
        """Инициализация адреса."""
        self.city = city
        self.street = street
        self.house = house

    def to_dict(self) -> Dict[str, str]:
        """Преобразование адреса в словарь для сериализации."""
        return {"city": self.city, "street": self.street, "house": self.house}

    @classmethod
    def from_dict(cls, d: Dict[str, str]) -> "Address":
        """Создание адреса из словаря."""
        return cls(d["city"], d["street"], d["house"])
