from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            f'Год выпуска {value} не может быть '
            f'больше текущего {timezone.now().year}!')
