from django.db import models


class WindDirectionChoices(models.TextChoices):
    N = 'north', 'Северный'
    NE = 'north-east', 'Северо-восточный'
    E = 'east', 'Восточный'
    SE = 'south-east', 'Юго-восточный'
    S = 'south', 'Южный'
    SW = 'south-west', 'Юго-западный'
    W = 'west', 'Западный'
    NW = 'north-west', 'Северо-западный'


class EventStatusChoices(models.TextChoices):
    PENDING = 'pending', 'Ещё не началось'
    GOING = 'going', 'Идёт сейчас'
    ENDED = 'ended', 'Закончилось'
