from django.conf import settings
from django.contrib.comments import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django import forms
from django.utils import timezone
from django.utils.encoding import force_text
from .settings import COMMENTS_EXCLUDE_FIELDS

from .models import PComment as Comment

from chapters.models import Chapter


class PCommentForm(CommentForm):
    """
    The comment form, applies various settings.
    """
    viewers = forms.ModelMultipleChoiceField(required=False,
                                             widget=forms.CheckboxSelectMultiple(),
                                             queryset=Chapter.objects.all())
                                             #TODO: should only be university chapters

    def __init__(self, *args, **kwargs):
        super(PCommentForm, self).__init__(*args, **kwargs)

        for name in COMMENTS_EXCLUDE_FIELDS:
            try:
                self.fields.pop(name)
            except KeyError:
                raise ImproperlyConfigured(
                    "Field name '{0}' in COMMENTS_EXCLUDE_FIELDS is invalid, it does not exist in the comment form.")

    def get_comment_model(self):
        return Comment

    def get_comment_create_data(self):
        # Fake form data for excluded fields, so there are no KeyError exceptions
        return dict(
            content_type = ContentType.objects.get_for_model(self.target_object),
            object_pk    = force_text(self.target_object._get_pk_val()),
            user_name    = "",
            user_email   = "",
            user_url     = "",
            comment      = self.cleaned_data["comment"],
            submit_date  = timezone.now(),
            site_id      = settings.SITE_ID,
            is_public    = True,
            is_removed   = False,
            #viewers      = self.cleaned_data["viewers"],
            )



