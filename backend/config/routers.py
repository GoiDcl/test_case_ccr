from rest_framework.routers import DefaultRouter

from event_app.viewsets import EventViewSet


router = DefaultRouter()

router.register(r'events', EventViewSet, basename='events')
