from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from core.apps.api.pagination import (
    get_paginated_response,
    LimitOffsetPagination,
)

from .serializers import (
    EventCreateSerializer,
    EventFilterSerializer,
    EventListSerializer,
    EventSerializer,
)
from .services import (
    BaseEventService,
    ORMEventService,
)


class EventListApi(APIView):

    @extend_schema(responses=EventListSerializer)
    def get(self, request):
        service: BaseEventService = ORMEventService()
        # Make sure the filters are valid, if passed
        filters_serializer = EventFilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        events = service.get_event_list()

        return get_paginated_response(
            pagination_class=LimitOffsetPagination,
            serializer_class=EventSerializer,
            queryset=events,
            request=request,
            view=self,
        )

    @extend_schema(
            request=EventCreateSerializer,
            responses=EventSerializer,
    )
    def post(self, request):
        service: BaseEventService = ORMEventService()

        serializer = EventCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event = service.event_create(
            **serializer.validated_data,  # type: ignore
        )

        serializer = EventSerializer(event)

        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class EventDetailApi(APIView):

    @extend_schema(
            responses=EventSerializer,
    )
    def get(self, request, event_id: int):
        service: BaseEventService = ORMEventService()
        try:
            event = service.get_event(event_id=event_id)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(event)

        return Response(serializer.data)

    @extend_schema(
            request=EventSerializer,
            responses=EventSerializer,
    )
    def put(self, request, event_id: int):
        service: BaseEventService = ORMEventService()
        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event = service.event_update(
            event_id=event_id,
            **serializer.validated_data,  # type: ignore
        )

        return Response(
            status=status.HTTP_200_OK,
            data=EventSerializer(event).data,
        )

    def delete(self, request, event_id):
        service: BaseEventService = ORMEventService()
        try:
            service.event_delete(event_id=event_id)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
