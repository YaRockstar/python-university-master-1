from abc import ABCMeta
from typing import Dict, Any


class VehicleMeta(ABCMeta):
    """Метакласс, автоматически регистрирующий подклассы Vehicle."""
    registry: Dict[str, type] = {}

    def __new__(mcls, name: str, bases: tuple, namespace: Dict[str, Any], **kwargs: Any) -> type:
        """Создание нового класса и его регистрация в реестре, если это подкласс Vehicle."""
        cls = super().__new__(mcls, name, bases, namespace)

        if name != "Vehicle" and not name.startswith("_"):
            key = name.lower()
            VehicleMeta.registry[key] = cls

        return cls
