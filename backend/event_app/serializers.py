from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from event_app.models import Event, EventLocation, WeatherForecast, EventImage


class WeatherForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherForecast
        fields = (
            'temperature',
            'humidity',
            'atmospheric_pressure',
            'wind_speed',
            'wind_direction',
        )


class EventLocationSerializer(serializers.ModelSerializer):
    weather = WeatherForecastSerializer(read_only=True)

    class Meta:
        model = EventLocation
        fields = (
            'name',
            'coordinates',
            'weather',
        )

    def validate_coordinates(self, value):
        try:
            longitude, latitude = value.split(';')
            longitude = float(longitude)
            latitude = float(latitude)
        except ValueError:
            raise serializers.ValidationError('Неправильный формат координат')
        return value


class EventImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)
    image_preview = serializers.ImageField(read_only=True)

    class Meta:
        model = EventImage
        fields = (
            'image',
            'image_preview',
        )


class EventSerializer(serializers.ModelSerializer):
    location = EventLocationSerializer(read_only=True)
    images = EventImageSerializer(many=True, read_only=True)
    published_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    starting_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    finishing_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Event
        fields = (
            'id',
            'name',
            'description',
            'published_at',
            'starting_at',
            'finishing_at',
            'creator',
            'location',
            'status',
            'rating',
            'images',
        )


class EventCreateSerializer(serializers.ModelSerializer):
    published_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    starting_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    finishing_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Event
        fields = (
            'id',
            'name',
            'description',
            'published_at',
            'starting_at',
            'finishing_at',
            'creator',
            'location',
            'status',
            'rating',
        )

    def validate(self, data):
        date_fields = ['published_at', 'starting_at', 'finishing_at']
        errors = {}
        for field in date_fields:
            if data[field] < timezone.now():
                errors[field] = 'Дата не может быть в прошлом!'
        if errors:
            raise ValidationError(errors)
        return data
