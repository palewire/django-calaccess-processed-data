import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = 'r269$heh9at2cot+5l$*$4&xzwsfbbg0&&^prr+e&oh)_4-+ga'
DEBUG = True
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_ROOT = os.path.join(BASE_DIR, ".static")
STATIC_URL = '/static/'
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]
ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'calaccess_raw',
    'calaccess_scraped',
    'calaccess_processed',
    'calaccess_processed_elections',
    'calaccess_processed_filings',
    'calaccess_processed_flatfiles',
    # 'calaccess_processed_campaignfinance',
    # 'toolbox',
    'opencivicdata.core.apps.BaseConfig',
    'opencivicdata.elections.apps.BaseConfig',
    # 'opencivicdata.campaign_finance.apps.BaseConfig',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'calaccess_processed',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
    },
    'loggers': {
        'calaccess_raw.management': {
            'handlers': ['console',],
            'level': 'DEBUG',
            'propagate': True,
        },
        'calaccess_scraped.management': {
            'handlers': ['console',],
            'level': 'DEBUG',
            'propagate': True,
        },
        'calaccess_processed': {
            'handlers': ['console',],
            'level': 'DEBUG',
            'propagate': True,
        },
        'calaccess_processed_campaignfinance': {
            'handlers': ['console',],
            'level': 'DEBUG',
            'propagate': True,
        },
        'calaccess_processed_elections': {
            'handlers': ['console',],
            'level': 'DEBUG',
            'propagate': True,
        },
        'calaccess_processed_filings': {
            'handlers': ['console',],
            'level': 'DEBUG',
            'propagate': True,
        },
        'calaccess_processed_flatfiles': {
            'handlers': ['console',],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

IA_STORAGE_ACCESS_KEY = os.getenv('IA_STORAGE_ACCESS_KEY')
IA_STORAGE_SECRET_KEY = os.getenv('IA_STORAGE_SECRET_KEY')
IA_STORAGE_COLLECTION = 'test_collection'
IA_STORAGE_CONTRIBUTOR = 'palewire'
IA_STORAGE_CREATOR = "palewire"
IA_STORAGE_PUBLISHER = 'california-civic-data-coalition/django-calaccess-processed-data'
IA_STORAGE_MEDIATYPE = "data"
IA_STORAGE_SUBJECT = ['test']

try:
    from .settings_local import *
except ImportError:
    pass
