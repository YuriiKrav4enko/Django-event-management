from django.urls import (
    include,
    path,
)


urlpatterns = [
    path("events/", include(("core.apps.events.urls", "events"))),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
]
