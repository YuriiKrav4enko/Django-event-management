from rest_framework import serializers

from core.apps.api.serializers import BaseListPaginatedResponseSerializer

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'id', 'title', 'description', 'date',
            'adress', 'lat', 'lon',
            'organizer',
        )


class EventListSerializer(BaseListPaginatedResponseSerializer):
    data = EventSerializer(many=True, read_only=True)  # type: ignore


class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'title', 'description', 'date',
            'adress', 'lat', 'lon',
            'organizer',
        )


class EventFilterSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)  # noqa
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    date = serializers.DateField(required=False)
