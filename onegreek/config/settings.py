# -*- coding: utf-8 -*-
"""
Django settings for onegreek project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import join

# See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
try:
    from S3 import CallingFormat
    AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN
except ImportError:
    # TODO: Fix this where even if in Dev this class is called.
    pass

from configurations import Configuration, values

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class Common(Configuration):

    ########## APP CONFIGURATION
    DJANGO_APPS = (
        # Default Django apps:
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.formtools',

        # Useful template tags:
        # 'django.contrib.humanize',

        # Admin
        'django.contrib.admin',
    )
    THIRD_PARTY_APPS = (
        'south',  # Database migration helpers:
        'crispy_forms',  # Form layouts
        'avatar',  # for user avatars
        'rest_framework',
        'akismet',
        'guardian',
        'djangular',
        'django_filters',
        'model_utils',
        'sorl.thumbnail',
        'tagging',
        'phonenumber_field',
        'jsonview',
    )

    # Apps specific for this project go here.
    LOCAL_APPS = (
        'apiroot',
        'utils',
        'core',
        'angularjs',
        'universities',
        'fraternities',
        #'sororities',
        'rush_forms',
        'chapters',
        'users',  # custom users app
        'django_comments',
        'rest_comments',
        'events',
        #'images',
    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

    INSTALLED_APPS += (
        # Needs to come last for now because of a weird edge case between
        #   South and allauth
        'allauth',  # registration
        'allauth.account',  # registration
        'allauth.socialaccount',  # registration
        'imagestore',
    )

    ########## END APP CONFIGURATION

    ########## MIDDLEWARE CONFIGURATION
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )
    ########## END MIDDLEWARE CONFIGURATION

    ########## DEBUG
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = values.BooleanValue(True)

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
    TEMPLATE_DEBUG = DEBUG
    ########## END DEBUG

    ########## SECRET CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
    # Note: This key only used for development and testing.
    #       In production, this is changed to a values.SecretValue() setting
    SECRET_KEY = "CHANGEME!!!"
    ########## END SECRET CONFIGURATION

    ########## FIXTURE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
    FIXTURE_DIRS = (
        join(BASE_DIR, 'fixtures'),
    )
    ########## END FIXTURE CONFIGURATION

    ########## EMAIL CONFIGURATION
    EMAIL_BACKEND = values.Value('django.core.mail.backends.smtp.EmailBackend')
    ########## END EMAIL CONFIGURATION

    ########## MANAGER CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
    ADMINS = (
        ('goldhand', 'will@django.nu'),
    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
    MANAGERS = ADMINS
    ########## END MANAGER CONFIGURATION

    ########## DATABASE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
    DATABASES = values.DatabaseURLValue('postgres://localhost/onegreek')
    ########## END DATABASE CONFIGURATION

    ########## CACHING
    # Do this here because thanks to django-pylibmc-sasl and pylibmc memcacheify is painful to install on windows.
    # memcacheify is what's used in Production
    CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
        }
    }
    ########## END CACHING

    ########## GENERAL CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
    TIME_ZONE = 'America/Phoenix'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
    LANGUAGE_CODE = 'en-us'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
    SITE_ID = 1

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
    USE_I18N = True

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
    USE_L10N = True

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
    USE_TZ = True
    ########## END GENERAL CONFIGURATION

    ########## TEMPLATE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        "allauth.account.context_processors.account",
        "allauth.socialaccount.context_processors.socialaccount",
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
        'django.core.context_processors.request',
        # Your stuff: custom template context processers go here
    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
    TEMPLATE_DIRS = (
        join(BASE_DIR, 'templates'),
    )

    TEMPLATE_LOADERS = (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )

    # See: http://django-crispy-forms.readthedocs.org/en/latest/install.html#template-packs
    CRISPY_TEMPLATE_PACK = 'bootstrap'
    ########## END TEMPLATE CONFIGURATION

    ########## STATIC FILE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
    STATIC_ROOT = join(os.path.dirname(BASE_DIR), 'static')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
    STATIC_URL = '/static/'

    # See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
    STATICFILES_DIRS = (
        join(BASE_DIR, 'static'),
    )

    # See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )
    ########## END STATIC FILE CONFIGURATION

    ########## MEDIA CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
    MEDIA_ROOT = join(BASE_DIR, 'media')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
    MEDIA_URL = '/media/'
    ########## END MEDIA CONFIGURATION

    ########## URL Configuration
    ROOT_URLCONF = 'config.urls'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
    WSGI_APPLICATION = 'config.wsgi.application'
    ########## End URL Configuration

    ########## AUTHENTICATION CONFIGURATION
    AUTHENTICATION_BACKENDS = (
        "django.contrib.auth.backends.ModelBackend",
        "guardian.backends.ObjectPermissionBackend",
        "allauth.account.auth_backends.AuthenticationBackend",
    )

    # Some really nice defaults
    ACCOUNT_AUTHENTICATION_METHOD = "email"
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_EMAIL_VERIFICATION = "false"
    # ACCOUNT_SIGNUP_FORM_CLASS = "users.forms.UserForm"
    # ACCOUNT_USER_DISPLAY = "users.user.get_full_name"
    #ACCOUNT_USERNAME_REQUIRED (=True)
    ########## END AUTHENTICATION CONFIGURATION


    ########## AUTHENTICATION PROVIDERS

    INSTALLED_APPS += (
        #'allauth.socialaccount.providers.bitly',
        #'allauth.socialaccount.providers.dropbox',
        'allauth.socialaccount.providers.facebook',
        #'allauth.socialaccount.providers.github',
        #'allauth.socialaccount.providers.google',
        #'allauth.socialaccount.providers.linkedin',
        #'allauth.socialaccount.providers.openid',
        #'allauth.socialaccount.providers.persona',
        #'allauth.socialaccount.providers.soundcloud',
        #'allauth.socialaccount.providers.stackexchange',
        #'allauth.socialaccount.providers.twitch',
        #'allauth.socialaccount.providers.twitter',
        #'allauth.socialaccount.providers.vimeo',
        #'allauth.socialaccount.providers.vk',
        #'allauth.socialaccount.providers.weibo',
    )

    SOCIALACCOUNT_PROVIDERS = \
        { 'facebook':
              { 'SCOPE': ['email', 'publish_stream',
                          'user_photos', 'user_hometown', 'user_location', 'photo_upload', 'status_update'],
                'AUTH_PARAMS': { 'auth_type': 'reauthenticate' },
                'METHOD': 'js_sdk',
                'VERIFIED_EMAIL': True
              }
        }

    ########## END AUTHENTICATION PROVIDERS


    ########## Custom user app defaults
    # Select the correct user model
    AUTH_USER_MODEL = "users.User"
    LOGIN_REDIRECT_URL = "users:redirect"
    ########## END Custom user app defaults

    ########## SLUGLIFIER
    AUTOSLUG_SLUGIFY_FUNCTION = "slugify.slugify"
    ########## END SLUGLIFIER

    ########## LOGGING CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
    # A sample logging configuration. The only tangible logging
    # performed by this configuration is to send an email to
    # the site admins on every HTTP 500 error when DEBUG=False.
    # See http://docs.djangoproject.com/en/dev/topics/logging for
    # more details on how to customize your logging configuration.
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
        }
    }
    ########## END LOGGING CONFIGURATION

    ########## COMMENTS CONFIGURATION

    COMMENTS_APP = 'rest_comments'
    COMMENTS_USE_EMAIL_NOTIFICATION = False
    COMMENTS_EXCLUDE_FIELDS = ('url', 'name', 'email')

    ########## END COMMENTS CONFIGURATION

    ########## DJANGO_GUARDIAN CONFIGURATION
    ANONYMOUS_USER_ID = -1
    ANONYMOUS_DEFAULT_USERNAME_VALUE = "ANON"

    ########## END DJANGO_GUARDIAN CONFIGURATION

    ########## DJANGO_REST_FRAMEWORK CONFIGURATION
    REST_FRAMEWORK = {
        'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
    }

    ########## END DJANGO_REST_FRAMEWORK CONFIGURATION

    ########## IMAGESTORE CONFIGURATION
    #IMAGESTORE_IMAGE_MODEL = 'images.models.Image'
    #IMAGESTORE_ALBUM_MODEL = 'images.models.Album'
    #IMAGESTORE_IMAGE_FORM = 'images.forms.ImageForm'
    #IMAGESTORE_ALBUM_FORM = 'images.forms.AlbumForm'
    IMAGESTORE_LOAD_CSS = True

    ########## END IMAGESTORE CONFIGURATION


    ########## Your common stuff: Below this line define 3rd party libary settings
    #SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'


class Local(Common):

    ########## INSTALLED_APPS
    INSTALLED_APPS = Common.INSTALLED_APPS
    ########## END INSTALLED_APPS

    ########## Mail settings
    DEFAULT_FROM_EMAIL = values.Value(
        'onegreek <onegreek-noreply@onegreek.org>')
    EMAIL_HOST = values.Value('smtp.sendgrid.com')
    EMAIL_HOST_PASSWORD = values.SecretValue(environ_prefix="", environ_name="SENDGRID_PASSWORD")
    EMAIL_HOST_USER = values.SecretValue(environ_prefix="", environ_name="SENDGRID_USERNAME")
    EMAIL_PORT = values.IntegerValue(587, environ_prefix="", environ_name="EMAIL_PORT")
    EMAIL_SUBJECT_PREFIX = values.Value('[onegreek] ', environ_name="EMAIL_SUBJECT_PREFIX")
    EMAIL_USE_TLS = True
    ########## End mail settings

    ########## django-debug-toolbar
    MIDDLEWARE_CLASSES = Common.MIDDLEWARE_CLASSES + ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += (
        'debug_toolbar',
        'django_extensions',
    )

    INTERNAL_IPS = ('127.0.0.1',)

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TEMPLATE_CONTEXT': True,
    }
    ########## end django-debug-toolbar

    ########## Your local stuff: Below this line define 3rd party libary settings
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'onegreek',                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': 'wpl',
            'PASSWORD': '',
            'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': '',                      # Set to empty string for default.
        }
    }


class Production(Common):

    ########## INSTALLED_APPS
    INSTALLED_APPS = Common.INSTALLED_APPS
    ########## END INSTALLED_APPS

    ########## SECRET KEY
    SECRET_KEY = values.SecretValue()
    ########## END SECRET KEY

    ########## django-secure
    INSTALLED_APPS += ("djangosecure", )

    # set this to 60 seconds and then to 518400 when you can prove it works
    #SECURE_HSTS_SECONDS = 60
    #SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(True)
    #SECURE_FRAME_DENY = values.BooleanValue(True)
    #SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(True)
    #SECURE_BROWSER_XSS_FILTER = values.BooleanValue(True)
    #SESSION_COOKIE_SECURE = values.BooleanValue(True)
    #SESSION_COOKIE_HTTPONLY = values.BooleanValue(True)
    #SECURE_SSL_REDIRECT = values.BooleanValue(True)
    ########## end django-secure

    ########## SITE CONFIGURATION
    # Hosts/domain names that are valid for this site
    # See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = ["*"]
    ########## END SITE CONFIGURATION

    INSTALLED_APPS += ("gunicorn", )

    ########## STORAGE CONFIGURATION
    # See: http://django-storages.readthedocs.org/en/latest/index.html
    INSTALLED_APPS += (
        'storages',
    )

    # See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
    STATICFILES_STORAGE = DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

    # See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
    AWS_ACCESS_KEY_ID = values.SecretValue()
    AWS_SECRET_ACCESS_KEY = values.SecretValue()
    AWS_STORAGE_BUCKET_NAME = values.SecretValue()
    AWS_AUTO_CREATE_BUCKET = True
    AWS_QUERYSTRING_AUTH = False

    # AWS cache settings, don't change unless you know what you're doing:
    AWS_EXPIREY = 60 * 60 * 24 * 7
    AWS_HEADERS = {
        'Cache-Control': 'max-age=%d, s-maxage=%d, must-revalidate' % (AWS_EXPIREY,
            AWS_EXPIREY)
    }

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
    STATIC_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
    ########## END STORAGE CONFIGURATION

    ########## EMAIL
    DEFAULT_FROM_EMAIL = values.Value(
            'onegreek <onegreek-noreply@onegreek.org>')
    EMAIL_HOST = values.Value('smtp.sendgrid.com')
    EMAIL_HOST_PASSWORD = values.SecretValue(environ_prefix="", environ_name="SENDGRID_PASSWORD")
    EMAIL_HOST_USER = values.SecretValue(environ_prefix="", environ_name="SENDGRID_USERNAME")
    EMAIL_PORT = values.IntegerValue(587, environ_prefix="", environ_name="EMAIL_PORT")
    EMAIL_SUBJECT_PREFIX = values.Value('[onegreek] ', environ_name="EMAIL_SUBJECT_PREFIX")
    EMAIL_USE_TLS = True
    SERVER_EMAIL = EMAIL_HOST_USER
    ########## END EMAIL

    ########## TEMPLATE CONFIGURATION

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )
    ########## END TEMPLATE CONFIGURATION

    ########## CACHING
    # Only do this here because thanks to django-pylibmc-sasl and pylibmc memcacheify is painful to install on windows.
    #CACHES = values.CacheURLValue(default="memcached://127.0.0.1:11211")

    os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';')
    os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
    os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')

    CACHES = {
        'default': {
            'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
            'TIMEOUT': 500,
            'BINARY': True,
            'OPTIONS': { 'tcp_nodelay': True }
        }
    }
    ########## END CACHING


    ########## Your production stuff: Below this line define 3rd party libary settings
