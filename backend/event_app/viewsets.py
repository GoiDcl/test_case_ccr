from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    inline_serializer,
    OpenApiParameter,
)
from rest_framework import viewsets, serializers

from common.permissions import SuperuserCUDAuthRetrievePublished, SuperuserCRUD
from event_app.filters import EventFilter
from event_app.models import Event, EventLocation
from event_app.serializers import EventSerializer, EventLocationSerializer, EventCreateSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Список мероприятий",
        description="Возвращает список мероприятий. Опционально можно отфильтровать по датам начала "
                    "и завершения, месту проведения, рейтингу и названию места проведения "
                    "или самого мероприятия.",
        parameters=[
            OpenApiParameter(
                name="starting",
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Фильтрация по дате начала.",
            ),
            OpenApiParameter(
                name="finishing",
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Фильтрация по дате завершения.",
            ),
            OpenApiParameter(
                name="location",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Фильтрация по названию места проведения.",
            ),
            OpenApiParameter(
                name="name",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Фильтрация по названию мероприятия.",
            ),
            OpenApiParameter(
                name="rating",
                type=OpenApiTypes.NUMBER,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Фильтрация по рейтингу.",
            ),
            OpenApiParameter(
                name="limit",
                type=OpenApiTypes.NUMBER,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Количество элементов на странице.",
            ),
            OpenApiParameter(
                name="page",
                type=OpenApiTypes.NUMBER,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Номер страницы.",
            ),
        ],
        responses={200: EventSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Мероприятие",
        description="Возвращает объект мероприятия.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                required=True,
                description="Уникальный идентификатор мероприятия.",
            ),
        ],
        responses={
            200: EventSerializer(),
            404: inline_serializer(
                name="GetEventsNotFound",
                fields={
                    "detail": serializers.CharField(default="No Event matches the given query.")
                },
            ),
        },
    ),
    create=extend_schema(
        summary="Создать мероприятие",
        description="Создаёт новый объект мероприятия.",
        responses={
            201: EventSerializer(),
            403: inline_serializer(
                name="EventsForbidden",
                fields={
                    "detail": serializers.CharField(default="Учётные данные не были предоставлены.")
                },
            ),
            404: inline_serializer(
                name="GetEventsNotFound",
                fields={
                    "detail": serializers.CharField(default="No Event matches the given query.")
                },
            ),
        },
    ),
    update=extend_schema(
        summary="Изменить мероприятие",
        description="Изменить объект мероприятия с указанием всех полей.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                required=True,
                description="Уникальный идентификатор мероприятия.",
            ),
        ],
        responses={
            200: EventSerializer(),
            403: inline_serializer(
                name="EventsForbidden",
                fields={
                    "detail": serializers.CharField(default="Учётные данные не были предоставлены.")
                },
            ),
            404: inline_serializer(
                name="GetEventsNotFound",
                fields={
                    "detail": serializers.CharField(default="No Event matches the given query.")
                },
            ),
        },
    ),
    partial_update=extend_schema(
        summary="Изменить мероприятие",
        description="Изменить объект мероприятия с указанием некоторых полей.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                required=True,
                description="Уникальный идентификатор мероприятия.",
            ),
        ],
        responses={
            200: EventSerializer(),
            403: inline_serializer(
                name="EventsForbidden",
                fields={
                    "detail": serializers.CharField(default="Учётные данные не были предоставлены.")
                },
            ),
            404: inline_serializer(
                name="GetEventsNotFound",
                fields={
                    "detail": serializers.CharField(default="No Event matches the given query.")
                },
            ),
        },
    ),
    destroy=extend_schema(
        summary="Удалить мероприятие",
        description="Удалить объект мероприятия.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                required=True,
                description="Уникальный идентификатор мероприятия.",
            ),
        ],
        responses={
            204: None,
            403: inline_serializer(
                name="EventsForbidden",
                fields={
                    "detail": serializers.CharField(default="Учётные данные не были предоставлены.")
                },
            ),
            404: inline_serializer(
                name="GetEventsNotFound",
                fields={
                    "detail": serializers.CharField(default="No Event matches the given query.")
                },
            ),
        },
    ),
)
@extend_schema(tags=["Мероприятия"])
class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [SuperuserCUDAuthRetrievePublished]
    filterset_class = EventFilter
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        queryset = Event.objects.prefetch_related('images', 'location__weather')
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(published_at__lte=timezone.now())

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EventCreateSerializer
        return EventSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Список мест проведения мероприятий",
        description="Возвращает список мест проведения мероприятий.",
        responses={200: EventLocationSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Место проведения мероприятий",
        description="Возвращает объект места проведения мероприятий.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                required=True,
                description="Уникальный идентификатор места.",
            ),
        ],
        responses={
            200: EventLocationSerializer(),
            404: inline_serializer(
                name="GetEventLocationsNotFound",
                fields={
                    "detail": serializers.CharField(
                        default="No EventLocation matches the given query."
                    )
                },
            ),
        },
    ),
    create=extend_schema(
        summary="Создать место проведения мероприятий",
        description="Создаёт новый объект места проведения мероприятий.",
        responses={
            201: EventLocationSerializer(),
            403: inline_serializer(
                name="EventLocationsForbidden",
                fields={
                    "detail": serializers.CharField(default="Учётные данные не были предоставлены.")
                },
            ),
            404: inline_serializer(
                name="GetEventLocationsNotFound",
                fields={
                    "detail": serializers.CharField(default="No EventLocation matches the given query.")
                },
            ),
        },
    ),
    update=extend_schema(
        summary="Изменить место проведения мероприятий",
        description="Изменить объект места проведения мероприятий с указанием всех полей.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                required=True,
                description="Уникальный идентификатор места.",
            ),
        ],
        responses={
            200: EventLocationSerializer(),
            403: inline_serializer(
                name="EventLocationsForbidden",
                fields={
                    "detail": serializers.CharField(default="Учётные данные не были предоставлены.")
                },
            ),
            404: inline_serializer(
                name="GetEventLocationsNotFound",
                fields={
                    "detail": serializers.CharField(default="No EventLocation matches the given query.")
                },
            ),
        },
    ),
    partial_update=extend_schema(
        summary="Изменить место проведения мероприятий",
        description="Изменить объект место проведений мероприятия с указанием некоторых полей.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                required=True,
                description="Уникальный идентификатор места.",
            ),
        ],
        responses={
            200: EventLocationSerializer(),
            403: inline_serializer(
                name="EventLocationsForbidden",
                fields={
                    "detail": serializers.CharField(default="Учётные данные не были предоставлены.")
                },
            ),
            404: inline_serializer(
                name="GetEventLocationsNotFound",
                fields={
                    "detail": serializers.CharField(default="No EventLocation matches the given query.")
                },
            ),
        },
    ),
    destroy=extend_schema(
        summary="Удалить место проведения мероприятий",
        description="Удалить объект место проведения мероприятий.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                required=True,
                description="Уникальный идентификатор места.",
            ),
        ],
        responses={
            204: None,
            403: inline_serializer(
                name="EventLocationsForbidden",
                fields={
                    "detail": serializers.CharField(default="Учётные данные не были предоставлены.")
                },
            ),
            404: inline_serializer(
                name="GetEventLocationsNotFound",
                fields={
                    "detail": serializers.CharField(default="No EventLocation matches the given query.")
                },
            ),
        },
    ),
)
@extend_schema(tags=["Места проведения мероприятий"])
class EventLocationViewSet(viewsets.ModelViewSet):
    queryset = EventLocation.objects.select_related('weather')
    serializer_class = EventLocationSerializer
    permission_classes = [SuperuserCRUD]
