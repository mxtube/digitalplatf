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

DEBUG = True

ALLOWED_HOSTS = [
    env('DOMAIN_NAME', default=''),
    'localhost',
    '0.0.0.0',  # noqa: S104
    '127.0.0.1',
    '[::1]',
]

# Application definition

INSTALLED_APPS += ['debug_toolbar',]


MIDDLEWARE += [
    # Django debug toolbar:
    # https://django-debug-toolbar.readthedocs.io
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = '/Users/mxtube/Pycharm/edu-digital-platform/docker_compose_volumes/dp_static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'core/static'),]


# MEDIA Files
# https://docs.djangoproject.com/en/5.0/ref/settings/#media-root

MEDIA_URL = '/media/'

MEDIA_ROOT = '/Users/mxtube/Pycharm/edu-digital-platform/docker_compose_volumes/dp_media/'
