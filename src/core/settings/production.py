import ssl
from .base import *

DEBUG = env.bool('DEBUG', False)

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# SECURITY Deploy on in production
# https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/#critical-settings

CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=False)

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=False)

SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)

SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=0)

SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=False)

SECURE_HSTS_PRELOAD = env.bool('SECURE_HSTS_PRELOAD', default=False)

# Application definition

INSTALLED_APPS += ['django_python3_ldap',]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/s/'

STATIC_ROOT = '/opt/dp_static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'core/static'),]


# MEDIA Files
# https://docs.djangoproject.com/en/5.0/ref/settings/#media-root

MEDIA_URL = '/m/'

MEDIA_ROOT = '/opt/dp_media/'

# DJANGO PYTHON3 LDAP
# https://github.com/etianen/django-python3-ldap

AUTHENTICATION_BACKENDS = ('django_python3_ldap.auth.LDAPBackend',)

LDAP_AUTH_URL = env('LDAP_AUTH_URL')
LDAP_AUTH_USE_TLS = False
LDAP_AUTH_TLS_VERSION = ssl.CERT_NONE
LDAP_AUTH_SEARCH_BASE = f'DC={env("LDAP_ASB_DC")},DC={env("LDAP_ASB_DC_POST")}'
LDAP_AUTH_OBJECT_CLASS = "OrganizationalPerson"

LDAP_AUTH_USER_FIELDS = {
    "username": "userPrincipalName",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
    "birthday": "pager",
    "middle_name": "middlename",
    "note": "description",
    "job_title": "title",
    "mobile": "mobile",
    "ldap_userpic": "thumbnailPhoto",
}

LDAP_AUTH_USER_LOOKUP_FIELDS = ("username",)
LDAP_AUTH_CLEAN_USER_DATA = "django_python3_ldap.utils.clean_user_data"
LDAP_AUTH_SYNC_USER_RELATIONS = "django_python3_ldap.utils.sync_user_relations"
LDAP_AUTH_FORMAT_SEARCH_FILTERS = "django_python3_ldap.utils.format_search_filters"
LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_active_directory"

ldap_connection_string = f"CN={env('LDAP_CN')},OU={env('LDAP_OU')},DC={env('LDAP_DC_PRE')},DC={env('LDAP_DC_POST')}"
LDAP_AUTH_CONNECTION_USERNAME = ldap_connection_string
LDAP_AUTH_CONNECTION_PASSWORD = env('LDAP_PASSWORD')

LDAP3_USER = os.getenv('LDAP3_USER')
LDAP3_PASSWORD = env('LDAP3_PASSWORD')

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django_python3_ldap": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}
