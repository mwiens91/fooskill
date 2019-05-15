"""
Django settings for fooskill project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG_RAW = os.environ["DEBUG"].lower()

if DEBUG_RAW == "false":
    DEBUG = False
elif DEBUG_RAW == "true":
    DEBUG = True
else:
    # Bad value in config file!
    raise ValueError("DEBUG must be True or False")

# Hosts - separate the comma-separated hosts and clean up any empty
# strings caused by a terminal comma in ".env"
ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].replace("'", "").split(",")
ALLOWED_HOSTS = list(filter(None, ALLOWED_HOSTS))

# Application definition

INSTALLED_APPS = [
    "api.apps.ApiConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "crispy_forms",
    "django_extensions",
    "django_filters",
    "drf_yasg",
    "rest_framework",
    "rest_framework.authtoken",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
]

ROOT_URLCONF = "fooskill.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "fooskill.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ["DATABASE_NAME"],
        "USER": os.environ["DATABASE_USER"],
        "PASSWORD": os.environ["DATABASE_USER_PASSWORD"],
        "HOST": os.environ["DATABASE_HOST"],
        "PORT": os.environ["DATABASE_PORT"],
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = os.environ["TIME_ZONE"]

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# User model to use

AUTH_USER_MODEL = "api.User"

# Django REST Framework settings

REST_FRAMEWORK = {
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "EXCEPTION_HANDLER": "rollbar.contrib.django_rest_framework.post_exception_handler",
}

# Swagger and ReDoc settings (see
# https://drf-yasg.readthedocs.io/en/stable/settings.html)
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Basic": {"type": "basic", "description": "Basic authentication"},
        "Token": {
            "type": "apiKey",
            "description": "Token authentication",
            "name": "Authorization",
            "in": "header",
        },
    }
}

# CORS settings - separate the comma-separated hostnames and clean up
# any empty strings caused by a terminal comma in ".env"
CORS_ORIGIN_WHITELIST = (
    os.environ["CORS_ORIGIN_WHITELIST"].replace("'", "").split(",")
)
CORS_ORIGIN_WHITELIST = list(filter(None, CORS_ORIGIN_WHITELIST))

# Rollbar error-tracking settings

ROLLBAR = {
    "access_token": os.environ["ROLLBAR_ACCESS_TOKEN"],
    "environment": "development" if DEBUG else "production",
    "branch": "master",
    "root": BASE_DIR,
}

# Glicko-2 settings

GLICKO2_BASE_RATING = float(os.environ["GLICKO2_BASE_RATING"])
GLICKO2_BASE_RD = float(os.environ["GLICKO2_BASE_RD"])
GLICKO2_BASE_VOLATILITY = float(os.environ["GLICKO2_BASE_VOLATILITY"])
GLICKO2_SYSTEM_CONSTANT = float(os.environ["GLICKO2_SYSTEM_CONSTANT"])
GLICKO2_RATING_PERIOD_DAYS = int(os.environ["GLICKO2_RATING_PERIOD_DAYS"])

# Other rating settings
NUMBER_OF_RATING_PERIODS_MISSED_TO_BE_INACTIVE = int(
    os.environ["NUMBER_OF_RATING_PERIODS_MISSED_TO_BE_INACTIVE"]
)
