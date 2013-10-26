from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.fields import SplitField, StatusField
from model_utils.models import StatusModel
from model_utils import Choices, FieldTracker
from model_utils.models import TimeStampedModel

from rest_framework.renderers import JSONRenderer

from core.models import Slugged


class Comment(TimeStampedModel, StatusModel):
    owner = models.ForeignKey('users.User', null=True, blank=True)
    STATUS = Choices(('draft', 'Draft'), ('public', 'Public'),
                     ('private', 'Share with members of your chapter'),
                     ('custom', 'Share with other chapters'))
    content = SplitField()
    viewers = models.ManyToManyField('chapters.Chapter', null=True, blank=True)

    def __unicode__(self):
        time = JSONRenderer().render(self.created)
        return '%s-%s' % (str(self.owner.id), time.strip('"'))

    def user_can_view(self, _user):
        if _user.chapter in self.viewers.all() or self.owner == _user:
            return True
        else:
            return False
