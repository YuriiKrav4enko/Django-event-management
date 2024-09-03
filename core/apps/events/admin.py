from urllib.parse import urlencode

from django.contrib import admin
from django.urls import reverse_lazy
from django.utils.html import format_html

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'description', 'date', 'adress', 'organizer_link',
    )

    def organizer_link(self, obj):
        url = reverse_lazy('admin:users_user_changelist')
        query = urlencode({'q': obj.organizer.email})
        return format_html(
            '<a target="_blank" href="{}?{}">{}</a>',
            url, query, obj.organizer.email,
        )
    organizer_link.short_description = 'Organizer'
