from django.contrib.auth import get_user_model
from django.db import models

from core.apps.common.fields import CoordinateField
from core.apps.common.models import TimedBaseModel

UserModel = get_user_model()


class Event(TimedBaseModel):
    title = models.CharField(
        verbose_name="Event's title",
        max_length=255,
    )
    description = models.TextField(
        verbose_name="Event's description",
        blank=True,
    )
    date = models.DateTimeField(
        verbose_name="Event's date",
    )
    organizer = models.ForeignKey(
        UserModel,
        related_name='events',
        on_delete=models.CASCADE,
        verbose_name="Organizer of the event",
    )
    # Location
    adress = models.CharField(
        verbose_name='Adress',
        max_length=255,
        blank=True,
        db_index=True
    )
    lat = CoordinateField(
        verbose_name='Latitude',
    )
    lon = CoordinateField(
        verbose_name='Longitude',
    )
