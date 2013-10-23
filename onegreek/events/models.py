from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.fields import SplitField, StatusField
from model_utils.models import TimeFramedModel
from model_utils import Choices, FieldTracker

from core.models import Slugged, Ownable


class Event(Slugged, Ownable, TimeFramedModel):
    STATUS = Choices(('draft', 'Draft'), ('public', 'Public'),
                     ('private', 'Share with members of your chapter'),
                     ('custom', 'Share with other chapters'))
    description = SplitField()
    viewers = models.ManyToManyField('chapters.Chapter', null=True, blank=True)
    attendees = models.ManyToManyField('users.User', null=True, blank=True)


    def get_chapter(self):
        return self.owner.chapter
