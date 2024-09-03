from abc import ABC, abstractmethod
from datetime import date, datetime
from decimal import Decimal

from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, AbstractUser

from .filters import BaseEventFilter
from .models import Event

UserModel = get_user_model()


class BaseEventService(ABC):
    @abstractmethod
    def get_event_list(
        self, filters: dict | None = None
    ) -> QuerySet[Event]:
        ...

    @abstractmethod
    def get_event(
        self, filters: dict | None = None
    ) -> QuerySet[Event]:
        ...
    
    @abstractmethod
    def event_create(
            self,
            title: str,
            description: str,
            date: datetime,
            organizer: AbstractBaseUser,
            adress: str,
            lat: int | None,
            lon: int | None,
        ) -> Event:
        ...


    @abstractmethod
    def event_update(
            self,
            event_id: int,
            title: str,
            description: str,
            date: datetime,
            organizer: AbstractBaseUser,
            adress: str,
            lat: int | None,
            lon: int | None,
        ) -> Event:
        ...

    @abstractmethod
    def event_delete(self, id: int) -> None:
        ...


class ORMEventService(BaseEventService):

    def get_event_list(self, filters: dict | None = None) -> QuerySet[Event]:
        filters = filters or {}

        qs = Event.objects.all()

        return BaseEventFilter(filters, qs).qs

    def get_event(self, id: int) -> Event | None:
        return get_object_or_404(Event, id=id)
    
    def event_create(
            self,
            title: str,
            description: str,
            date: datetime,
            organizer: AbstractBaseUser,
            adress: str,
            lat: int | None,
            lon: int | None,
        ) -> Event:
        event = Event(
            title=title,
            description=description,
            date=date,
            organizer=organizer,
            adress=adress,
            lat=lat,
            lon=lon
        )
        event.full_clean()
        event.save()
        return event


    def event_update(
            self,
            event_id: int,
            title: str,
            description: str,
            date: datetime,
            organizer: AbstractUser,
            adress: str,
            lat: Decimal | None,
            lon: Decimal | None,
        ) -> Event:
        event = get_object_or_404(Event, id=event_id)
        event.title = title
        event.description = description
        event.date = date
        event.organizer = organizer
        event.adress = adress
        event.lat = lat
        event.lon = lon

        event.save()
        return event


    def event_delete(self, id: int) -> None:
        event = get_object_or_404(Event, id=id)
        event.delete()
