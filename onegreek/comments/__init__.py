from django.core.urlresolvers import reverse_lazy
from .models import PComment as Comment
from .forms import PCommentForm as CommentForm

def get_model():
    """
    Return the model to use for commenting.
    """
    return Comment


def get_form():
    """
    Return the form to use for commenting.
    """
    return CommentForm

def get_form_target():
    return reverse_lazy('pcomment-list')