from .models import RestComment
from .forms import RestCommentForm

def get_model():
    return RestComment

def get_form():
    return RestCommentForm
