class InvalidVehicleError(ValueError):
    """Исключение, которое выбрасывается, если ТС содержит некорректные данные."""


class PermissionDeniedError(PermissionError):
    """Исключение, которое выбрасывается при отсутствии прав доступа."""


class DriverNotFoundError(LookupError):
    """Исключение, которое выбрасывается, если водитель не найден."""
