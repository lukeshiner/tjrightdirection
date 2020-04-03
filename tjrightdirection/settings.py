"""
Django settings for tjrightdirection project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

import toml
from django.core.exceptions import ImproperlyConfigured

TRAVIS_ENVIRONMENT = "TRAVIS" in os.environ

SOURCE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
BASE_DIR = os.path.dirname(SOURCE_DIR)
CONFIG_DIR = os.path.join(BASE_DIR, "config")

CONFIG_PATH = os.path.join(CONFIG_DIR, "config.toml")

try:
    with open(CONFIG_PATH, "r") as config_file:
        CONFIG = toml.load(config_file)
except Exception:
    raise ImproperlyConfigured("Config file not found.")


def get_config(key):
    """Return the associated value for key from the config file."""
    value = CONFIG.get(key)
    if value is None:
        raise ImproperlyConfigured(f"Config value '{key}' is not set.")
    else:
        return value


# Secret Key
try:
    secret_key_path = os.path.join(CONFIG_DIR, "secret_key.toml")
    with open(secret_key_path, "r") as secret_key_file:
        SECRET_KEY = toml.load(secret_key_file)["SECRET_KEY"]
except Exception:
    raise ImproperlyConfigured(
        "A secret key must be set in tjrightdirection/secret_key.toml"
    )

DEBUG = get_config("DEBUG")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": get_config("DATABASE_HOST"),
        "NAME": get_config("DATABASE_NAME"),
        "USER": get_config("DATABASE_USER"),
        "PASSWORD": get_config("DATABASE_PASSWORD"),
        "PORT": get_config("DATABASE_PORT"),
        "TEST": {"NAME": get_config("TEST_DATABASE_NAME")},
    }
}
ALLOWED_HOSTS = get_config("ALLOWED_HOSTS")
ADMINS = get_config("ADMINS")
EMAIL_HOST = get_config("EMAIL_HOST")
EMAIL_HOST_USER = get_config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = get_config("EMAIL_HOST_PASSWORD")
EMAIL_PORT = get_config("EMAIL_PORT")
EMAIL_USE_TLS = get_config("EMAIL_USE_TLS")
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "adminsortable2",
    "tjhome",
    "gallery",
    "recomendations",
    "contact",
    "hitcounter",
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

ROOT_URLCONF = "tjrightdirection.urls"

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
                "django.template.context_processors.static",
                "django.template.context_processors.media",
            ],
        },
    },
]

WSGI_APPLICATION = "tjrightdirection.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "Europe/London"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
