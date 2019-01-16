from .base import *
import dj_database_url
# Add your domain to allowed hosts:

ALLOWED_HOSTS = [
    'djangoauth.herokuapp.com',
]

DEBUG = True

STATIC_ROOT = "static/"

DATABASES['default'] = dj_database_url.config(
    conn_max_age=600, ssl_require=True)

# Static FILES
MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# Name and email tuple of admins who get notifications on server exceptions
ADMINS = (
  (os.environ.get('ADMIN_NAME'), os.environ.get('ADMIN_EMAIL'),
))