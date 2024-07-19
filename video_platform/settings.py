"""
Django settings for video_platform project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import json
import os
import base64
import dj_database_url
from pathlib import Path
from google.oauth2 import service_account


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-e2ei)&uz_g6n=*cli@ysq3^i_cd2zk1u-%i22f+0-xza%&1mar"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", ".vercel.app", ".herokuapp.com"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "vpapp",
    "rest_framework",
    "rest_framework.authtoken",
    "storages",
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
}


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "video_platform.middleware.DisableCSRFMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "noreply.vpapp@gmail.com"
EMAIL_HOST_PASSWORD = "nkicuoghxuajhyni"

ROOT_URLCONF = "video_platform.urls"

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

WSGI_APPLICATION = "video_platform.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
# }
DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": BASE_DIR / "db.sqlite3",
    # }
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv('DATABASE_NAME'),
        "USER": os.getenv('DATABASE_USER'),
        "PASSWORD":os.getenv('DATABASE_PASS'),
        "HOST": os.getenv('DATABASE_HOST'),
        "PORT": os.getenv('DATABASE_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

GS_BUCKET_NAME = 'vpapp_videos'

google_credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
if google_credentials_json:
    google_credentials_json = base64.b64decode(google_credentials_json).decode('utf-8')
    google_credentials = json.loads(google_credentials_json)
else:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable not set.")

GS_CREDENTIALS = service_account.Credentials.from_service_account_info(google_credentials)

STATIC_URL = "https://storage.googleapis.com/vpapp_videos/static/"
STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
MEDIA_URL = "https://storage.googleapis.com/vpapp_videos/media/"
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"



# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
