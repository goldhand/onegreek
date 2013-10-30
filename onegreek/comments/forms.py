from django.contrib.comments import CommentForm
from django.core.exceptions import ImproperlyConfigured
from django import forms
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
                    "Field name '{0}' in FLUENT_COMMENTS_EXCLUDE_FIELDS is invalid, it does not exist in the comment form.")

    def get_comment_model(self):
        return Comment

    def get_comment_create_data(self):
        # Fake form data for excluded fields, so there are no KeyError exceptions
        for name in COMMENTS_EXCLUDE_FIELDS:
            self.cleaned_data[name] = ""
        data = super(PCommentForm, self).get_comment_create_data()
        return data



