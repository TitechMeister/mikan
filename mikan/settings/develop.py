# flake8: noqa
from .base import *
import logging

DEBUG = True

INTERNAL_IPS = ('127.0.0.1',)

MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] +=(
        'rest_framework.authentication.SessionAuthentication',
)

CORS_ORIGIN_WHITELIST = [
    '127.0.0.1:*',
    'localhost:*',
]

CORS_ORIGIN_ALLOW_ALL = True

# For debugging
if DEBUG:
    # will output to your console
    logging.basicConfig(
        level = logging.DEBUG,
        format = '%(asctime)s %(levelname)s %(message)s',
    )
