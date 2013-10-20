from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.fields import SplitField, StatusField
from model_utils.models import StatusModel
from model_utils import Choices, FieldTracker

from core.models import Slugged


class Chapter(Slugged, StatusModel):

    STATUS = Choices('excellence', 'achievement', 'probation', 'inactive')
    description = SplitField()
    awards = SplitField()
    philanthropy = SplitField()
    potential_new_members = SplitField()
    facebook = models.URLField(blank=True)
    fb_status = models.TextField(blank=True)
    cost = models.IntegerField()
    gpa = models.FloatField()

    _tracker = FieldTracker()



