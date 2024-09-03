from abc import (
    ABC,
    abstractmethod,
)
from datetime import datetime
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404

from anymail.exceptions import (
    AnymailError,
    AnymailRequestsAPIError,
)
from sentry_sdk import capture_exception
from templated_email import send_templated_mail

from core.apps.emails.utils import get_default_email_context
from core.apps.users.models import User

from .filters import BaseEventFilter
from .models import Event


UserModel = get_user_model()


class BaseEventService(ABC):
    @abstractmethod
    def get_event_list(
        self, filters: dict | None = None,
    ) -> QuerySet[Event]:
        ...

    @abstractmethod
    def get_event(
        self, filters: dict | None = None,
    ) -> QuerySet[Event]:
        ...

    @abstractmethod
    def event_create(
            self,
            title: str,
            description: str,
            date: datetime,
            organizer: User,
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
            organizer: User,
            adress: str,
            lat: int | None,
            lon: int | None,
    ) -> Event:
        ...

    @abstractmethod
    def event_delete(self, event_id: int) -> None:  # noqa A002
        ...


class ORMEventService(BaseEventService):

    def get_event_list(self, filters: dict | None = None) -> QuerySet[Event]:
        filters = filters or {}

        qs = Event.objects.all()

        return BaseEventFilter(filters, qs).qs

    def get_event(self, event_id: int) -> Event | None:
        return get_object_or_404(Event, id=event_id)

    def _send_event_create_email(
            self,
            user: User,
            event: Event,
    ) -> None:  # TODO make as celery task
        try:
            email_address = user.email
            context = get_default_email_context()
            context.update(
                name=user.name,
                title=event.title,
                date=event.date,
                adress=event.adress,
            )
            send_templated_mail(
                template_name='event_creation_notification.email',  # TODO change tamplate
                recipient_list=[email_address],
                from_email=settings.TEMPLATED_EMAIL_FROM_EMAIL,
                context=context,
            )
        except (AnymailRequestsAPIError, AnymailError, Exception) as anymail_error:
            capture_exception(anymail_error)

    def event_create(
            self,
            title: str,
            description: str,
            date: datetime,
            organizer: User,
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
            lon=lon,
        )
        event.full_clean()
        event.save()
        self._send_event_create_email(
            user=organizer,
            event=event,
        )
        return event

    def event_update(
            self,
            event_id: int,
            title: str,
            description: str,
            date: datetime,
            organizer: User,
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
        event.lat = lat  # type: ignore
        event.lon = lon  # type: ignore

        event.save()
        return event

    def event_delete(self, event_id: int) -> None:
        event = get_object_or_404(Event, id=event_id)
        event.delete()
