from .base import *
import dj_database_url
# Add your domain to allowed hosts:

ALLOWED_HOSTS = [
    'djangoauth.herokuapp.com',
]

DEBUG = False

DATABASES['default'] = dj_database_url.config(
    conn_max_age=600, ssl_require=True)