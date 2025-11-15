import logging

logger = logging.getLogger("transport_company")


class LoggingMixin:
    """Добавление логирования действий с ТС."""

    def log_action(self, message: str) -> None:
        """Логирование действий с транспортным средством."""
        logger.info(f"[LOG] {message}")


class NotificationMixin:
    """Добавление отправки уведомлений."""

    def send_notification(self, message: str) -> None:
        """Отправка уведомления."""
        logger.info(f"[NOTIFY] {message}")
