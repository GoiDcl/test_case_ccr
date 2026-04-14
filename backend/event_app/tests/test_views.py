from datetime import timedelta

import pytest
from django.utils import timezone
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APIClient

from event_app.models import Event
from event_app.tests.factories import EventLocationFactory, PastEventFactory, FutureEventFactory


@pytest.mark.django_db
def test_user_get_event():
    api_client = APIClient()
    location = EventLocationFactory()
    past_events = [PastEventFactory(location=location) for _ in range(5)]
    future_events = [FutureEventFactory(location=location) for _ in range(5)]

    url = reverse_lazy('events-list')
    response = api_client.get(url)
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data['results']) == len(past_events)
    assert future_events[0].id not in response_data['results']


@pytest.mark.django_db
def test_superuser_get_event(super_user):
    api_client = APIClient()
    api_client.force_login(super_user)
    location = EventLocationFactory()
    events = [PastEventFactory(location=location) for _ in range(5)]
    future_events = [FutureEventFactory(location=location) for _ in range(5)]

    url = reverse_lazy('events-list')
    response = api_client.get(url)
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data['results']) == len(events) + len(future_events)


@pytest.mark.django_db
def test_user_create_event():
    api_client = APIClient()
    location = EventLocationFactory()
    event_data = {
        'name': 'test',
        'published_at': timezone.now() + timedelta(days=1),
        'starting_at': timezone.now() + timedelta(days=1, hours=1),
        'finishing_at': timezone.now() + timedelta(days=1, hours=2),
        'location': location,
    }

    url = reverse_lazy('events-list')
    response = api_client.post(url, event_data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_superuser_create_event(super_user):
    api_client = APIClient()
    api_client.force_login(super_user)
    location = EventLocationFactory()
    event_data = {
        'name': 'test',
        'published_at': timezone.now() + timedelta(days=1),
        'starting_at': timezone.now() + timedelta(days=1, hours=1),
        'finishing_at': timezone.now() + timedelta(days=1, hours=2),
        'location': location.id,
    }

    url = reverse_lazy('events-list')
    response = api_client.post(url, event_data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_superuser_create_invalid_event(super_user):
    api_client = APIClient()
    api_client.force_login(super_user)
    location = EventLocationFactory()
    event_data = {
        'name': 'test',
        'published_at': timezone.now() - timedelta(days=1),
        'starting_at': timezone.now() - timedelta(days=1, hours=1),
        'finishing_at': timezone.now() - timedelta(days=1, hours=2),
        'location': location.id,
    }

    url = reverse_lazy('events-list')
    response = api_client.post(url, event_data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_user_update_event():
    api_client = APIClient()
    location = EventLocationFactory()
    event = PastEventFactory(location=location)
    event_data = {
        'name': 'test',
    }

    url = reverse_lazy('events-detail', args=[event.id])
    response = api_client.patch(url, data=event_data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_superuser_update_event(super_user):
    api_client = APIClient()
    api_client.force_login(super_user)
    location = EventLocationFactory()
    event = PastEventFactory(location=location)
    event_data = {
        'name': 'test',
    }

    url = reverse_lazy('events-detail', args=[event.id])
    response = api_client.patch(url, data=event_data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_delete_event():
    api_client = APIClient()
    location = EventLocationFactory()
    event = PastEventFactory(location=location)

    url = reverse_lazy('events-detail', args=[event.id])
    response = api_client.delete(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_superuser_delete_event(super_user):
    api_client = APIClient()
    api_client.force_login(super_user)
    location = EventLocationFactory()
    event = PastEventFactory(location=location)
    assert Event.objects.count() == 1

    url = reverse_lazy('events-detail', args=[event.id])
    response = api_client.delete(url)
    assert response.status_code == 204
    assert Event.objects.count() == 0


@pytest.mark.django_db
def test_user_access_event_location():
    api_client = APIClient()
    location = EventLocationFactory()
    create_data = {
        'name': 'test',
        'coordinates': '123.123;321.321'
    }
    update_data = {
        'name': 'test',
    }

    list_url = reverse_lazy('locations-list')
    detail_url = reverse_lazy('locations-detail', args=[location.id])
    response = api_client.get(list_url)
    assert response.status_code == 403
    response = api_client.get(detail_url)
    assert response.status_code == 403
    response = api_client.post(list_url, create_data)
    assert response.status_code == 403
    response = api_client.patch(detail_url, update_data)
    assert response.status_code == 403
    response = api_client.delete(detail_url, update_data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_superuser_access_event_location(super_user):
    api_client = APIClient()
    api_client.force_login(super_user)
    location = EventLocationFactory()
    create_data = {
        'name': 'test',
        'coordinates': '123.123;321.321'
    }
    update_data = {
        'name': 'test',
    }

    list_url = reverse_lazy('locations-list')
    detail_url = reverse_lazy('locations-detail', args=[location.id])
    response = api_client.get(list_url)
    assert response.status_code == 200
    response = api_client.get(detail_url)
    assert response.status_code == 200
    response = api_client.post(list_url, create_data)
    assert response.status_code == 201
    response = api_client.patch(detail_url, update_data)
    assert response.status_code == 200
    response = api_client.delete(detail_url, update_data)
    assert response.status_code == 204
