from django.contrib.contenttypes.models import ContentType
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


def color_key(status, component=None):
    if status == "chapter":
        _class = "error"
        if component == "btn":
            _class = "danger"
    elif status == "pledge":
        _class = "success"
    elif status == "rush":
        _class = "info"
    elif status == "active":
        _class = "warning"
    else:
        _class = ""
    if component == "table":
        return _class
    else:
        return "%s-%s" % (component, _class)


class Event(TimeFramedModel, StatusModel, Slugged):
    owner = models.ForeignKey('users.User', null=True, blank=True, related_name='events')
    STATUS = Choices(
        ('rush', 'Rushees'),
        ('pledge', 'Pledges'),
        ('active', 'Actives'),
        ('call', 'Call List'),
        ('public', 'Public'),
    )
    description = SplitField()
    all_day = models.BooleanField(default=False)
    #attendees = models.ManyToManyField('users.User', null=True, blank=True, related_name='attending')

    enable_comments = models.BooleanField("Enable comments", default=True)

    # Optional reverse relation, allow ORM querying:
    #comments_set = CommentsRelation()

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'pk': self.pk})

    def get_api_url(self):
        return "/events/#/events/%d" % self.id

    def get_chapter(self):
        if self.owner:
            return self.owner.chapter
        else:
            return None

    def get_status_text_class(self):
        return color_key(self.status, "text")

    def get_attendees_object(self):
        if not self.attendees_set.all():
            attendees = Attendees.objects.create(event=self)
        else:
            attendees = self.attendees_set.filter(active=True)[0]
        return attendees

    def get_attendees(self):
        attendees_obj = self.get_attendees_object()
        return attendees_obj.attendees.all()

    def get_rsvps(self):
        attendees_obj = self.get_attendees_object()
        return attendees_obj.rsvps.all()

    def get_rsvps_not_attendees(self):
        attendees_obj = self.get_attendees_object()
        return attendees_obj.rsvps.exclude(attending__id=attendees_obj.id)

    def get_rsvp_url(self):
        return reverse("events:rsvp", kwargs={'event_id': self.id})

    def get_attend_url(self):
        return reverse("events:attend", kwargs={'event_id': self.id})

    def get_content_type_id(self):
        return ContentType.objects.get_for_model(self).id



@receiver(signals.post_save, sender=Event)
def set_group(sender, **kwargs):
    event = kwargs.get('instance')
    chapter = event.owner.chapter
    # remove any existing perms
    for group in chapter.groups.all():
        remove_perm('view_event', group, event)

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
                assign_perm('view_event', chapter_group, event)

    if not 'change_event' in get_perms(event.owner, event):
        assign_perm('change_event', event.owner, event)
        assign_perm('delete_event', event.owner, event)
    assign_perm('change_event', chapter.linked_admin_group, event)
    assign_perm('delete_event', chapter.linked_admin_group, event)


class Attendees(models.Model):
    event = models.ForeignKey(Event)
    active = models.BooleanField(default=1)
    rsvps = models.ManyToManyField('users.User', null=True, blank=True, related_name='rsvps')
    rsvps_copy = models.ManyToManyField('users.User', null=True, blank=True, related_name='rsvps_copy')
    attendees = models.ManyToManyField('users.User', null=True, blank=True, related_name='attending')

    def save(self, *args, **kwargs):
        #self.rsvps_copy = self.rsvps.exclude(attending__id=self.id)
        return super(Attendees, self).save()

    def title(self):
        return self.event.title

    def start(self):
        return self.event.start

    def end(self):
        return self.event.end

    def status(self):
        return self.event.status



#Event.attendees_set = property(lambda e: Attendees.objects.get_or_create(event=e)[0])

from calendar import HTMLCalendar
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc


class EventCalendar(HTMLCalendar):
    def __init__(self, events):
        super(EventCalendar, self).__init__()
        self.events = self.group_by_day(events)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = "day %s %s" % (self.cssclasses[weekday], "span2")
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.events:
                cssclass += ' filled'
                body = ['<ul class="unstyled">']
                for event in self.events[day]:
                    body.append('<li>')
                    body.append('<a href="%s" class="%s %s">' % (event.get_api_url(),
                                                                 event.status,
                                                                 color_key(event.status, "text"))
                    )
                    body.append(esc(event.title))
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday span2', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(EventCalendar, self).formatmonth(year, month)

    def group_by_day(self, events):
        field = lambda event: event.start.day
        return dict(
            [(day, list(items)) for day, items in groupby(events, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)


