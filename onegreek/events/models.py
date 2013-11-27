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
    STATUS = Choices(
        ('draft', 'Draft'),
        ('public', 'Public'),
        ('chapter', 'Your Chapter'),
        ('rush', 'Rushes'),
        ('pledge', 'Pledges'),
        ('active', 'Actives')
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
            ('add_event', 'add_event'),
            ('change_event', 'change_event'),
            ('delete_event', 'delete_event'),
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
    chapter = event.owner.chapter
    chapter_groups = []
    if event.status == 'public':
        chapter_groups = [chapter.linked_group]
    if event.status == 'chapter':
        chapter_groups = [chapter.linked_group]
    if event.status == 'rush':
        chapter_groups = [
            chapter.linked_rush_group,
            chapter.linked_active_group
        ]
    if event.status == 'pledge':
        chapter_groups = [
            chapter.linked_pledge_group,
            chapter.linked_active_group
        ]
    if event.status == 'active':
        chapter_groups = [chapter.linked_active_group]

    if chapter_groups:
        for chapter_group in chapter_groups:
            if not 'view_event' in get_perms(chapter_group, event):
                print 'adding view perm to %s' % chapter_group.name
                assign_perm('view_event', chapter_group, event)
                assign_perm('change_event', chapter_group, event)

    if not 'change_event' in get_perms(event.owner, event):
        assign_perm('change_event', event.owner, event)
        assign_perm('delete_event', event.owner, event)

