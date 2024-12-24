"""
This file contains all the settings that defines the development server.
SECURITY WARNING: don't run with debug turned on in production!
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from core.settings.components import env, BASE_DIR
from core.settings.components.common import (
    INSTALLED_APPS,
    MIDDLEWARE,
)

DEBUG = False

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
