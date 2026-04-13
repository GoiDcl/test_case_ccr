from django_filters import CharFilter, DateTimeFromToRangeFilter, FilterSet, NumericRangeFilter

from event_app.models import Event


class EventFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='iexact')
    location = CharFilter(
        field_name='location__name',
        lookup_expr='istartswith',
        label='Целевая рабочая станция'
    )
    rating = NumericRangeFilter(field_name='rating', lookup_expr='range')
    starting = DateTimeFromToRangeFilter(field_name='starting_at')
    finishing = DateTimeFromToRangeFilter(field_name='finishing_at')

    class Meta:
        model = Event
        fields = ()
