from rest_framework import serializers


class BaseListPaginatedResponseSerializer(serializers.Serializer):
    offset = serializers.IntegerField()
    limit = serializers.IntegerField()
    count = serializers.IntegerField()
    next = serializers.URLField()  # noqa: A003
    previous = serializers.URLField()
