from pathlib import Path

import environ


env = environ.Env(
    DEBUG=(bool, False),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

environ.Env.read_env(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = []


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth',
    'dj_rest_auth.registration',
]

FIRST_PARTY_APPS = [
    'core.apps.users',
    'core.apps.emails',
    'core.apps.events',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + FIRST_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'core.project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {

}

# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", default=True)
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "email"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_ADAPTER = "core.apps.auth.adapters.AccountAdapter"

SITE_ID = 1

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend

if env.str('MAILGUN_API_KEY', '') and env.str('MAILGUN_SENDER_DOMAIN', ''):
    EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
    ANYMAIL = {
        'MAILGUN_API_KEY': env.str('MAILGUN_API_KEY'),
        'MAILGUN_SENDER_DOMAIN': env.str('MAILGUN_SENDER_DOMAIN'),
    }
    if env.str('MAILGUN_API_URL'):
        ANYMAIL['MAILGUN_API_URL'] = env.str('MAILGUN_API_URL')
else:
    # django-environ - The email() method is an alias for email_url().
    EMAIL_CONFIG = env.email_url('DJANGO_EMAIL_CONFIG', default='consolemail://')
    vars().update(EMAIL_CONFIG)

DEFAULT_FROM_EMAIL = 'Yurii Kravchenko <yuriy.krav4enko28@gmail.com>'

# django-templated-email
# -----------------------------------------------------------------------------
TEMPLATED_EMAIL_BACKEND = 'templated_email.backends.vanilla_django.TemplateBackend'
TEMPLATED_EMAIL_FROM_EMAIL = DEFAULT_FROM_EMAIL


# SENTRY SETTINGS
# -----------------------------------------------------------------------------
if SENTRY_DSN := env.str('SENTRY_DSN', ''):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()]
    )
