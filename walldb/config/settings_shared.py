import os
import sys

from django.core.urlresolvers import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '../')
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'bootstrap3',

    'apps.walldb',
    'apps.wallpaper',
    'apps.user',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
ROOT_URLCONF = 'walldb.urls'
WSGI_APPLICATION = 'walldb.wsgi.application'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Amsterdam'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

AUTH_PROFILE_MODULE = 'user.UserProfile'

AUTHENTICATION_BACKENDS = (
    'apps.user.authentication_backends.EmailAuthenticationBackend',
)

REST_FRAMEWORK = {
    'PAGE_SIZE': 5,
    'MAX_PAGINATE_BY': 100,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    )
}

LOGIN_URL = reverse_lazy('walldb:user:auth-login')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
    }
}

MAX_AVATAR_FILE_SIZE = 100  # in kilobytes
