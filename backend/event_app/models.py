from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from imagekit.processors import ResizeToFit

from common.fields import JpegImageSpecField
from event_app.constants import WindDirectionChoices, EventStatusChoices


class EventLocation(models.Model):
    name: str = models.CharField(
        verbose_name='Название',
        max_length=255,
    )
    coordinates: str = models.TextField(
        verbose_name='Координаты',
    )

    class Meta:
        verbose_name: str = 'Место проведения мероприятия'
        verbose_name_plural: str = 'Места проведения мероприятий'

    def __str__(self):
        return self.name


class WeatherForecast(models.Model):
    location: EventLocation = models.OneToOneField(
        verbose_name='Место проведения мероприятия',
        to=EventLocation,
        on_delete=models.CASCADE,
        related_name='weather',
    )
    temperature: int = models.IntegerField(
        verbose_name='Температура, в градусах Цельсия',
        validators=[MinValueValidator(-90), MaxValueValidator(60)],
    )
    humidity: str = models.IntegerField(
        verbose_name='Влажность воздуха, в процентах',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    atmospheric_pressure: int = models.IntegerField(
        verbose_name='Атмосферное давление, в мм ртутного столба',
        validators=[MinValueValidator(650), MaxValueValidator(820)],
    )
    wind_direction: int = models.CharField(
        verbose_name='Направление ветра',
        choices=WindDirectionChoices.choices,
        default=WindDirectionChoices.N,
    )
    wind_speed: int = models.IntegerField(
        verbose_name='Скорость ветра, в м/с',
        validators=[MinValueValidator(0)],
    )

    class Meta:
        verbose_name: str = 'Погода в месте проведения мероприятия'
        verbose_name_plural: str = 'Погода в местах проведения мероприятий'

    def __str__(self):
        return self._meta.verbose_name


class Event(models.Model):
    location: EventLocation = models.ForeignKey(
        verbose_name='Место проведения',
        to=EventLocation,
        on_delete=models.CASCADE,
        related_name='events',
    )
    name: str = models.CharField(
        verbose_name='Название',
        max_length=255,
    )
    description: str = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True,
    )
    published_at: datetime = models.DateTimeField(
        verbose_name='Дата и время публикации',
    )
    starting_at: datetime = models.DateTimeField(
        verbose_name='Дата и время начала',
    )
    finishing_at: datetime = models.DateTimeField(
        verbose_name='Дата и время завершения',
    )
    creator: str = models.CharField(
        verbose_name='Автор',
        max_length=255,
        null=True,
        blank=True,
    )
    rating: int = models.IntegerField(
        verbose_name='Рейтинг',
        validators=[MinValueValidator(0), MaxValueValidator(25)],
        null=True,
        blank=True,
    )
    status: str = models.CharField(
        verbose_name='Статус',
        choices=EventStatusChoices.choices,
        default=EventStatusChoices.PENDING,
    )

    class Meta:
        verbose_name: str = 'Мероприятие'
        verbose_name_plural: str = 'Мероприятия'
        ordering: tuple[str] = ('name', 'starting_at', 'finishing_at')

    def __str__(self):
        return f"{self.name} {self.starting_at:%Y-%m-%d}"

    def save(self, *args, **kwargs):
        if self.id is None:
            if (
                self.published_at < timezone.now() or
                self.starting_at < timezone.now() or
                self.finishing_at < timezone.now()
            ):
                raise ValidationError('Нельзя установить прошедшую дату для нового мероприятия')

    def send_email(self):
        to = ['123@lol.com']
        context = {
            'location_name': self.location.name,
            'coordinates': self.location.coordinates,
            'finishing_at': self.finishing_at,
            'description': self.description,
        }
        message = render_to_string('events/email.html', context)
        subject = f'Мероприятие {self.name} началось!'
        send_mail(subject, message, settings.SERVER_EMAIL, to, html_message=message)


class EventImage(models.Model):
    event: Event = models.ForeignKey(
        verbose_name='Мероприятие',
        to=Event,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.FileField(
        verbose_name='Изображение',
        upload_to='event_images',
    )
    image_preview = JpegImageSpecField(
        source='image',
        processors=[ResizeToFit(200, 200, upscale=False)],
    )

    class Meta:
        verbose_name: str = 'Изображение мероприятия'
        verbose_name_plural: str = 'Изображения мероприятий'
