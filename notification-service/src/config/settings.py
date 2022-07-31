import os
from pathlib import Path

from split_settings.tools import include

include(
    "components/database.py",
    # "components/logging.py",
)

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG", "True") == "True"
FAKE_API = os.environ.get("FAKE_API", "True") == "True"
FAKE_EMAIL_PROVIDER = os.environ.get("FAKE_EMAIL_PROVIDER", "True") == "True"


ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1 localhost").split(" ")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_beat",
    "ckeditor",
    "distributions.apps.DistributionsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# MONGO settings
MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
MONGO_DB = os.environ.get("MONGO_DB", "test_db")
MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION", "test_collection")

# REDIS settings
broker_host = os.environ.get("BROKER_HOST", "localhost")
broker_port = int(os.environ.get("BROKER_PORT", 6379))

# Auth API config
AUTH_HOST = os.environ.get("AUTH_HOST", "localhost")
AUTH_PORT = int(os.environ.get("AUTH_PORT", 82))
AUTH_URL = "https://{AUTH_HOST}:{AUTH_PORT}/api/v1/user/{USER_ID}"

# sendgrid token
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
EMAIL = os.environ.get("EMAIL", "ealmina@yandex.ru")
