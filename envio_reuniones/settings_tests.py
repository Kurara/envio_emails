from envio_reuniones.settings import *

ALLOWED_HOSTS = ['localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(process)d/%(thread)d/{}/%(module)s:%(lineno)d %(levelname)s: %(message)s'	
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'console': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'cycle.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'INFO',
        },
        'cycle_mails': {
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'INFO',
        },
    }
}

LANGUAGE_CODE = 'es-es'