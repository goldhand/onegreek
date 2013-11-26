from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group, Permission

from model_utils.fields import SplitField, StatusField
from model_utils.models import TimeFramedModel, StatusModel
from model_utils import Choices, FieldTracker

#from comments.utils import CommentsRelation

from guardian.shortcuts import assign_perm, get_perms, remove_perm

from core.models import Slugged
from core.models import unique_slug, base_concrete_model


class Event(TimeFramedModel, StatusModel, Slugged):
    owner = models.ForeignKey('users.User', null=True, blank=True, related_name='events')
    STATUS = Choices(('draft', 'Draft'), ('public', 'Public'),
                     ('chapter', 'Share with all members of your chapter'),
                     ('rush', 'Share with rush group'),
                     ('pledge', 'Share with Pledge group'),
                     ('active', 'Share with Active Chapter')
    )
    description = SplitField()
    #viewers = models.ManyToManyField('chapters.Chapter', null=True, blank=True)
    #No longer needed, will instead add view_event permissions to groups selected in form
    attendees = models.ManyToManyField('users.User', null=True, blank=True, related_name='attending')

    enable_comments = models.BooleanField("Enable comments", default=True)

    # Optional reverse relation, allow ORM querying:
    #comments_set = CommentsRelation()

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        permissions = (
            ('view_event', 'view_event'),
        )

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'pk': self.pk})

    def get_chapter(self):
        if self.owner:
            return self.owner.chapter
        else:
            return None


@receiver(signals.post_save, sender=Event)
def set_group(sender, **kwargs):
    event = kwargs.get('instance')
    chapter_group = event.owner.chapter.linked_group
    if event.status == 'rush':
        chapter_group = event.owner.chapter.linked_rush_group

    if chapter_group:
        if not 'view_event' in get_perms(chapter_group, event):
            print 'adding permissions'
            assign_perm('view_event', chapter_group, event)
        if not 'change_event' in get_perms(event.owner, event):
            assign_perm('change_event', event.owner, event)

