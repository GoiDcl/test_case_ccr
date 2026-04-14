from django.core.validators import MinValueValidator
from django.utils import timezone
from django.utils.deconstruct import deconstructible


@deconstructible
class NotPastDateTimeValidator(MinValueValidator):
    """Проверяет, что дата и время не находятся в прошлом."""

    message = 'Убедитесь, что дата и время не находятся в прошлом.'

    def __init__(self, limit_value=timezone.now(), message=None):
        super().__init__(limit_value, message)
