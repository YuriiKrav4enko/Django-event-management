from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'id', 'title', 'description', 'date',
            'adress', 'lat', 'lon',
            'organizer'
        )


class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'title', 'description', 'date',
            'adress', 'lat', 'lon',
            'organizer'
        )


class EventFilterSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    date = serializers.DateField(required=False)
