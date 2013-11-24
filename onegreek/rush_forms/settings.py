"""
Default settings for the ``onegreek.forms`` app. Each of these can be
overridden in your project's settings module, just like regular
Django settings. The ``editable`` argument for each controls whether
the setting is editable via Django's admin.

Thought should be given to how a setting is actually used before
making it editable, as it may be inappropriate - for example settings
that are only read during startup shouldn't be editable, since changing
them would require an application reload.
"""
from __future__ import unicode_literals

from django.conf import settings


def get(key, default):
    getattr(settings, key, default)




FORMS_FIELD_MAX_LENGTH = get(
    #"Max length allowed for field values in the forms app.",
    "FORMS_FIELD_MAX_LENGTH",
    2000,
    )


FORMS_LABEL_MAX_LENGTH = get(
    #"Max length allowed for field labels in the forms app.",
    "FORMS_LABEL_MAX_LENGTH",
    200,
    )

FORMS_CSV_DELIMITER = get(
    #"Char to use as a field delimiter when exporting form responses as CSV.",
    "FORMS_CSV_DELIMITER",
    ",",
    )

FORMS_UPLOAD_ROOT = get(
    #"Absolute path for storing file uploads for the forms app.",
    "FORMS_UPLOAD_ROOT",
    "",
)

FORMS_EXTRA_FIELDS = get(
    "FORMS_EXTRA_FIELDS",
    (),
)

FORMS_USE_HTML5 = get(
    #"Use html5",
    "FORMS_USE_HTML5",
    True,
    )
