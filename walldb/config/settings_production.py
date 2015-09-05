from .settings_shared import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['.walldb.net']

STATIC_ROOT = '/var/www/walldb/static/'
MEDIA_ROOT = '/var/www/walldb/media/'

LOGGING['handlers'] = {
    'console': {
        'class': 'logging.StreamHandler',
        'formatter': 'simple',
        'level': 'INFO'
    },
    'logfile': {
        'class': 'logging.handlers.WatchedFileHandler',
        'filename': '/var/log/walldb/error.log',
        'level': 'WARNING'
    },
}

LOGGING['loggers'] = {
    '': {
        'handlers': ['console', 'logfile'],
        'propagate': True,
        'level': 'INFO',
    },
    'django': {
        'handlers': ['console', 'logfile'],
        'propagate': False,
        'level': 'INFO'
    }
}
