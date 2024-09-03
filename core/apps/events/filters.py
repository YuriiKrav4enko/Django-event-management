import django_filters

from .models import Event


class BaseEventFilter(django_filters.FilterSet):
    class Meta:
        model = Event
        fields = ("id", "title", "description", "date", "organizer")
