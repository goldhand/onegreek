from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

AKISMET_API_KEY = getattr(settings, 'AKISMET_API_KEY', None)
AKISMET_BLOG_URL = getattr(settings, 'AKISMET_BLOG_URL', None)  # Optional, to override auto detection
AKISMET_IS_TEST = getattr(settings, 'AKISMET_IS_TEST', False)   # Enable in case of testing

CRISPY_TEMPLATE_PACK = getattr(settings, 'CRISPY_TEMPLATE_PACK', 'bootstrap')

USE_THREADEDCOMMENTS = 'threadedcomments' in settings.INSTALLED_APPS

COMMENTS_REPLACE_ADMIN = getattr(settings, "COMMENTS_REPLACE_ADMIN", True)

CONTENTS_USE_AKISMET = getattr(settings, 'CONTENTS_USE_AKISMET', bool(AKISMET_API_KEY))
COMMENTS_USE_EMAIL_NOTIFICATION = getattr(settings, 'COMMENTS_USE_EMAIL_NOTIFICATION', True)  # enable by default
COMMENTS_CLOSE_AFTER_DAYS = getattr(settings, 'COMMENTS_CLOSE_AFTER_DAYS', None)
COMMENTS_MODERATE_AFTER_DAYS = getattr(settings, 'COMMENTS_MODERATE_AFTER_DAYS', None)
COMMENTS_AKISMET_ACTION = getattr(settings, 'COMMENTS_AKISMET_ACTION', 'moderate')  # or 'delete'

COMMENTS_EXCLUDE_FIELDS = getattr(settings, 'COMMENTS_EXCLUDE_FIELDS', ()) or ()

if COMMENTS_AKISMET_ACTION not in ('moderate', 'delete'):
    raise ImproperlyConfigured("COMMENTS_AKISMET_ACTION can be 'moderate' or 'delete'")

