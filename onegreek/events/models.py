from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.fields import SplitField, StatusField
from model_utils.models import TimeFramedModel
from model_utils import Choices, FieldTracker

#from comments.utils import CommentsRelation

from core.models import Slugged


class Event(TimeFramedModel, Slugged):
    owner = models.ForeignKey('users.User', null=True, blank=True, related_name='events')
    STATUS = Choices(('draft', 'Draft'), ('public', 'Public'),
                     ('private', 'Share with members of your chapter'),
                     ('custom', 'Share with other chapters'))
    description = SplitField()
    viewers = models.ManyToManyField('chapters.Chapter', null=True, blank=True)
    attendees = models.ManyToManyField('users.User', null=True, blank=True, related_name='attending')

    enable_comments = models.BooleanField("Enable comments", default=True)

    # Optional reverse relation, allow ORM querying:
    #comments_set = CommentsRelation()

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'pk': self.pk})

    def get_chapter(self):
        return self.owner.chapter

    def user_can_view(self, _user):
        if _user.chapter in self.viewers.all() or self.owner == _user:
            return True
        else:
            return False

