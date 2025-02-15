from django.urls import path

from .apis import (
    EventDetailApi,
    EventListApi,
)


urlpatterns = [
    path("", EventListApi.as_view(), name="event-list"),
    path("<int:event_id>/", EventDetailApi.as_view(), name="event-detail"),
]
