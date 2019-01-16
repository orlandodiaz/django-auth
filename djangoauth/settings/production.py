from .base import *
import dj_database_url

DEBUG = False

# Name and email tuple of admins who get notifications on server exceptions
# Be sure to have SERVER_EMAIL set
SERVER_EMAIL = DEFAULT_FROM_EMAIL
ADMINS = [(os.environ.get('ADMIN_NAME'), os.environ.get('ADMIN_EMAIL')),]

# Add your domain to allowed hosts:

ALLOWED_HOSTS = [
    'djangoauth.herokuapp.com',
]


DATABASES['default'] = dj_database_url.config(
    conn_max_age=600, ssl_require=True)

# Static FILES
STATIC_ROOT = "static/"

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]


