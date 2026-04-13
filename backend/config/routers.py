from rest_framework.routers import DefaultRouter

from event_app.viewsets import EventViewSet, EventLocationViewSet

router = DefaultRouter()

router.register(r'events', EventViewSet, basename='events')
router.register(r'locations', EventLocationViewSet, basename='locations')
