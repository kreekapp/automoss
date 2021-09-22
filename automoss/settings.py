"""
Django settings for automoss project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from .redis import REDIS_URL
from .apps.utils.core import capture_in
from .apps.utils.core import first
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'automoss.apps.jobs',
    'automoss.apps.reports',
    'automoss.apps.api',
    'automoss.apps.users',
    'automoss.apps.results',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'automoss.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Global templates directory
        'DIRS': [BASE_DIR / 'automoss' / 'templates'],
        # Search local application templates directories
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

WSGI_APPLICATION = 'automoss.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# If running unit tests, create an in-memory sqlite3 database.
# Otherwise, create a mysql database
DATABASE_ENGINE = 'sqlite3' if 'test' in sys.argv else 'mysql'

DATABASES = {
    'default': {
        'ENGINE': f'django.db.backends.{DATABASE_ENGINE}',
        'NAME': os.getenv("DB_NAME"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': '3306',

        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'users.User'

LOGIN_REDIRECT_URL = '/jobs/'
LOGIN_URL = "/user/login/"
# Currently returns logged_out.html
#LOGOUT_REDIRECT_URL = '/accounts/login'

#EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.getenv("EMAIL_PORT")

DEFAULT_FROM_EMAIL = "noreply@automoss.co.za"

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Johannesburg'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# +-----------------+
# | CUSTOM SETTINGS |
# +-----------------+

# Celery variables
BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


# Default (None) is the number of CPUs available on your system.
# TODO min(num processors, 4)
CELERY_CONCURRENCY = 4  # None

# Contexts
LANGUAGE_CONTEXT = {}
with capture_in(LANGUAGE_CONTEXT):
    # Supported languages

    # https://github.com/highlightjs/highlight.js/blob/main/SUPPORTED_LANGUAGES.md

    SUPPORTED_LANGUAGES = {
        # CODE : (Name, moss_name, [extensions], highlight_name)
        'PY': ('Python', 'python', ['py'], 'python'),  # pyi, pyc, pyd, pyo, pyw, pyz
        'JA': ('Java', 'java', ['java'], 'java'),  # class, jar
        'CP': ('C++', 'cc', ['C', 'cc', 'cpp', 'cxx', 'c++', 'h', 'H', 'hh', 'hpp', 'hxx', 'h++'], 'cpp'),
        'CX': ('C', 'c', ['c', 'h'], 'c'),
        'CS': ('C#', 'csharp', ['cs', 'csx'], 'csharp'),
        'JS': ('Javascript', 'javascript', ['js'], 'javascript'),  # cjs, mjs
        'PL': ('Perl', 'perl', ['pl', 'plx', 'pm', 'xs', 't', 'pod'], 'perl'),
        'MP': ('MIPS assembly', 'mips', ['asm', 's'], 'x86asm'),

        # TODO decide which to add, and add extensions
        # 'LP' : ('Lisp', 'lisp', []),
        # 'HS' : ('Haskell', 'haskell', []),
        # 'VB' : ('Visual Basic', 'vb', []),
        # 'MB' : ('Matlab', 'matlab', []),
        # 'AA' : ('a8086 assembly', 'a8086', []),
        # 'VL' : ('Verilog', 'verilog', []),
        # 'PS' : ('Pascal', 'pascal', []),
        # 'ML' : ('ML', 'ml', []),
        # 'AD' : ('Ada', 'ada', []),
        # 'VH' : ('VHDL', 'vhdl', []),
        # 'SC' : ('Scheme', 'scheme', []),
        # 'FT' : ('FORTRAN', 'fortran', ['f', 'for', 'f90']),
        # 'SP' : ('Spice', 'spice', []),
        # 'PG' : ('Prolog', 'prolog', ['pl', 'pro', 'P']),
        # 'PS' : ('PL/SQL', 'plsql', []),
        # 'AS' : ('ASCII', 'ascii', []) # All?
    }

ARCHIVE_CONTEXT = {}
with capture_in(ARCHIVE_CONTEXT):
    SUPPORTED_ARCHIVES = ["rar", "tar", "tar.bz2", "tar.gz", "tar.xz", "zip"]

MOSS_CONTEXT = {}
with capture_in(MOSS_CONTEXT):
    # Moss defaults
    READABLE_LANGUAGE_MAPPING = {
        SUPPORTED_LANGUAGES[l][0]: l for l in SUPPORTED_LANGUAGES}
    DEFAULT_MOSS_SETTINGS = {
        'max_until_ignored': 10,
        'max_displayed_matches': 250
    }

STATUS_CONTEXT = {}
with capture_in(STATUS_CONTEXT):
    # Statuses
    INQUEUE_STATUS = 'INQ'
    UPLOADING_STATUS = 'UPL'
    PROCESSING_STATUS = 'PRO'
    PARSING_STATUS = 'PAR'
    COMPLETED_STATUS = 'COM'
    FAILED_STATUS = 'FAI'

    STATUSES = {
        # 'Code': 'Name',
        INQUEUE_STATUS: 'In Queue',
        UPLOADING_STATUS: 'Uploading',
        PROCESSING_STATUS: 'Processing',
        PARSING_STATUS: 'Parsing',
        COMPLETED_STATUS: 'Completed',
        FAILED_STATUS: 'Failed'
    }

SUBMISSION_CONTEXT = {}
with capture_in(SUBMISSION_CONTEXT):
    # Submission types
    BASE_FILES_NAME = 'base_files'
    FILES_NAME = 'files'

    SUBMISSION_TYPES = {
        BASE_FILES_NAME: 'Base file',
        FILES_NAME: 'Submission'
    }

JOB_CONTEXT = {}
with capture_in(JOB_CONTEXT):
    JOB_UPLOAD_TEMPLATE = f'{MEDIA_ROOT}/{{job_id}}/uploads'
    SUBMISSION_UPLOAD_TEMPLATE = f'{JOB_UPLOAD_TEMPLATE}/{{file_type}}/{{file_id}}'

    MIN_RETRY_TIME = 32
    MAX_RETRY_TIME = 256
    MAX_RETRY_DURATION = 86400
    EXPONENTIAL_BACKOFF_BASE_RANGE = [1, 2]#1.5  # 1.5  # 1<=x<=2
    FIRST_RETRY_INSTANT = True

JOB_EVENT_CONTEXT = {}
with capture_in(JOB_EVENT_CONTEXT):
    INQUEUE_EVENT = 'INQ'
    UPLOADING_EVENT = 'UPL'
    PROCESSING_EVENT = 'PRO'
    PARSING_EVENT = 'PAR'
    COMPLETED_EVENT = 'COM'
    FAILED_EVENT = 'FAI'
    RETRY_EVENT = 'RET'
    ERROR_EVENT = 'ERR'

    EVENTS = {
        INQUEUE_EVENT: 'Placed in the processing queue',
        UPLOADING_EVENT: 'Started uploading to MOSS',
        PROCESSING_EVENT: 'Started processing',
        PARSING_EVENT: 'Started parsing',
        COMPLETED_EVENT: 'Job completed',
        FAILED_EVENT: 'Job failed',
        RETRY_EVENT: 'Retrying job',
        ERROR_EVENT: 'An error occurred'
    }


# UI Defaults
UI_CONTEXT = {}
with capture_in(UI_CONTEXT):
    POLLING_TIME = 1000  # in milliseconds
    MOSS_POLLING_TIME = 30000  # in milliseconds

# Misc Constants
UUID_LENGTH = 36
MAX_COMMENT_LENGTH = 64
