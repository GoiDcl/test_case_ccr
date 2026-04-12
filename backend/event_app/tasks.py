from collections import namedtuple
from random import randint, choice

from celery import shared_task
from django.utils import timezone
from openpyxl.reader.excel import load_workbook

from event_app.constants import WindDirectionChoices
from event_app.models import Event, EventLocation, WeatherForecast


def _find_cell_name(workbook):
    """Находим столбец с названиями мероприятий"""
    cell_tuple = namedtuple('CellFlat', ['col', 'row'])
    try:
        for w in workbook:
            for l in w:
                if str(l.value).strip() == 'Название':
                    return cell_tuple(l.column, l.row)
    except Exception:
        raise

@shared_task
def import_excel_events_file_task(excel_file):
    """Загрузка файла Excel со старыми ценами квартир."""
    workbook = load_workbook(excel_file, read_only=True)
    wb = workbook.active
    cellname = _find_cell_name(wb)
    events_dict = {}
    locations_dict = {}

    for row in wb.iter_rows(min_row=cellname.row + 1):
        event_name = row[cellname.col - 1].value
        description = row[cellname.col].value
        published = row[cellname.col + 1].value
        starting = row[cellname.col + 2].value
        finishing = row[cellname.col + 3].value
        location_name = row[cellname.col + 4].value
        coordinates = row[cellname.col + 5].value
        rating = row[cellname.col + 6].value


        if event_name and event_name != 'Название':
            locations_dict[location_name] = {
                'name': location_name,
                'coordinates': coordinates,
            }
            events_dict[event_name] = {
                'name': event_name,
                'description': description,
                'published_at': published,
                'starting_at': starting,
                'finishing_at': finishing,
                'rating': rating,
                'location_name': location_name,
            }
    existing_locations = {
        location.name: location
        for location in EventLocation.objects.all()
    }
    locations_to_create = [
        EventLocation(**data)
        for name, data in locations_dict.items()
        if name not in existing_locations
    ]
    if locations_to_create:
        EventLocation.objects.bulk_create(locations_to_create)

    existing_events = set(
        Event.objects.filter(name__in=events_dict).values_list('name', flat=True)
    )
    events_to_create = []
    for name, data in events_dict.items():
        if name in existing_events:
            continue
        location_name = data.pop('location_name')
        location = existing_locations.get(location_name)
        events_to_create.append(Event(**data, location=location))
    if events_to_create:
        Event.objects.bulk_create(events_to_create)


@shared_task
def check_event_statuses():
    events = Event.objects.filter(status=EventStatusChoices.PENDING)
    events_to_update = []
    events_to_notify = []
    for event in events:
        if event.starting_at > timezone.now():
            event.status = EventStatusChoices.GOING
            events_to_update.append(event)
            events_to_notify.append(event)
        if event.finishing_at > timezone.now():
            event.status = EventStatusChoices.ENDED
            events_to_update.append(event)
    if events_to_update:
        Event.objects.bulk_update(events_to_update, ['status'])
    if events_to_notify:
        for event in events_to_notify:
            event.send_email()

@shared_task
def weather_forecasts_update_task():
    locations = EventLocation.objects.all()
    fields = ["temperature", "humidity", "atmospheric_pressure", "wind_direction", "wind_speed"]
    forecasts = []
    new_forecasts = []
    for location in locations:
        temperature = randint(-90, 60)
        humidity = randint(0, 100)
        atmospheric_pressure = randint(650, 820)
        wind_direction = choice(WindDirectionChoices.values)
        wind_speed = randint(0, 100)
        try:
            forecast = location.weather
            location.weather.temperature = temperature
            location.weather.humidity = humidity
            location.weather.atmospheric_pressure = atmospheric_pressure
            location.weather.wind_direction = wind_direction
            location.weather.wind_speed = wind_speed
            forecasts.append(forecast)
        except EventLocation.weather.RelatedObjectDoesNotExist:
            new_forecast = WeatherForecast(
                location=location,
                temperature=temperature,
                humidity=humidity,
                atmospheric_pressure=atmospheric_pressure,
                wind_direction=wind_direction,
                wind_speed=wind_speed,
            )
            new_forecasts.append(new_forecast)

    if forecasts:
        WeatherForecast.objects.bulk_update(forecasts, fields)
    if new_forecasts:
        WeatherForecast.objects.bulk_create(new_forecasts)

