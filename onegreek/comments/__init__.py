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
