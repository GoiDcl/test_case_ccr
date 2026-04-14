import factory
from factory import fuzzy, Faker, LazyAttribute, Iterator
from factory.django import DjangoModelFactory

from event_app.constants import EventStatusChoices
from event_app.models import Event, EventLocation


class EventLocationFactory(DjangoModelFactory):
    name = Faker("word")
    coordinates = LazyAttribute(
        lambda _: f"{Faker('latitude')};{Faker('longitude')}"
    )

    class Meta:
        model = EventLocation


class EventFactory(DjangoModelFactory):
    name = Faker("word")
    description = Faker("sentence")
    creator = Faker("name")
    rating = fuzzy.FuzzyInteger(0, 25)
    status = Iterator([choice[0] for choice in EventStatusChoices.choices])

    class Meta:
        model = Event


class PastEventFactory(EventFactory):
    published_at = Faker("past_datetime")
    starting_at = Faker("past_datetime")
    finishing_at = Faker("past_datetime")


class FutureEventFactory(EventFactory):
    published_at = Faker("future_datetime")
    starting_at = Faker("future_datetime")
    finishing_at = Faker("future_datetime")
