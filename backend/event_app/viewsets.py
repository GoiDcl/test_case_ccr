from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from common.permissions import SuperuserCUDAuthRetrievePublished, SuperuserCRUD
from event_app.filters import EventFilter
from event_app.models import Event
from event_app.serializers import EventSerializer, EventLocationSerializer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [SuperuserCUDAuthRetrievePublished]
    filterset_class = EventFilter
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        queryset = Event.objects.prefetch_related('images', 'location__weather')
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(published_at__lte=timezone.now())


class EventLocationViewSet(viewsets.ModelViewSet):
    serializer_class = EventLocationSerializer
    permission_classes = [SuperuserCRUD]
