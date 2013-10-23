from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.fields import SplitField, StatusField
from model_utils.models import StatusModel
from model_utils import Choices, FieldTracker

from core.models import Slugged


class University(Slugged):
    pass
