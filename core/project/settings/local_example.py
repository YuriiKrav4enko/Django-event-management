from .main import *  # noqa


# GENERAL
# ------------------------------------------------------------------------------
DEBUG = True

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# drf-spectacular
# https://drf-spectacular.readthedocs.io/en/latest/readme.html
INSTALLED_APPS += ["drf_spectacular"]  # noqa F405
REST_FRAMEWORK['DEFAULT_SCHEMA_CLASS'] = 'drf_spectacular.openapi.AutoSchema'  # noqa F405
