from .base import *

DEBUG = True

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# Application definition

INSTALLED_APPS += ['debug_toolbar',]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware',]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = '/Users/mxtube/Pycharm/edu-digital-platform/docker_compose_volumes/dp_static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'core/static'),]


# MEDIA Files
# https://docs.djangoproject.com/en/5.0/ref/settings/#media-root

MEDIA_URL = '/media/'

MEDIA_ROOT = '/Users/mxtube/Pycharm/edu-digital-platform/docker_compose_volumes/dp_media/'
