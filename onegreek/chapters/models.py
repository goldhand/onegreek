from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import signals
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver

from model_utils.fields import SplitField, StatusField
from model_utils.models import StatusModel
from model_utils import Choices, FieldTracker

from core.models import Slugged, base_concrete_model, unique_slug
from rush_forms.models import Form, Field


class Chapter(Slugged, StatusModel):
    STATUS = Choices('excellence', 'achievement', 'probation', 'inactive')
    fraternity = models.ForeignKey('fraternities.Fraternity', null=True, blank=True)
    university = models.ForeignKey('universities.University', null=True, blank=True)
    fraternity_title = models.CharField(max_length=255, blank=True)
    university_title = models.CharField(max_length=255, blank=True)
    description = SplitField(blank=True)
    location = models.TextField(blank=True)
    awards = SplitField(blank=True)
    philanthropy = SplitField(blank=True)
    potential_new_members = SplitField(blank=True)
    facebook = models.URLField(blank=True)
    fb_status = models.TextField(blank=True)
    cost = models.IntegerField(blank=True, null=True)
    gpa = models.FloatField(blank=True, null=True)
    groups = models.ManyToManyField(Group, null=True, blank=True)
    linked_group = models.OneToOneField(Group, null=True, blank=True, related_name='linked_chapter')
    linked_rush_group = models.OneToOneField(Group, null=True, blank=True, related_name='linked_chapter_rush')
    linked_pending_group = models.OneToOneField(Group, null=True, blank=True, related_name='linked_chapter_pending')
    rush_form = models.OneToOneField('rush_forms.Form', null=True, blank=True, related_name="chapter")

    _tracker = FieldTracker()

    class Meta:
        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"
        permissions = (
            ('view_chapter', 'view_chapter'),
        )

    def get_absolute_url(self):
        return reverse('chapters:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.fraternity and not self.fraternity_title:
            self.fraternity_title = self.fraternity.title
        if self.university and not self.university_title:
            self.university_title = self.university.title
        return super(Chapter, self).save(*args, **kwargs)

    def get_rush_form(self, *args, **kwargs):
        if not self.rush_form:
            self.rush_form = Form.objects.create()
            self.rush_form.title = "Chapter_%d Rush Form" % self.id
            _field = Field(
                form=self.rush_form,
                label="Legacy?",
                field_type=1,
                required=False
            )
            _field.save()
            self.rush_form.fields.add(_field)
            self.rush_form.save()
            self.save()
        return self.rush_form

    def get_groups(self, *args, **kwargs):
        if not self.groups.all():
            self.groups.add(self.linked_group)
            self.groups.add(self.linked_rush_group)
            self.groups.add(self.linked_pending_group)
        return self.groups.all()


@receiver(signals.post_save, sender=Chapter)
def set_group(sender, **kwargs):
    if kwargs.get('created'):
        chapter = kwargs.get('instance')
        group = Group.objects.get_or_create(name="%s_%d %s" % ("chapter", chapter.id, chapter.title))
        rush_group = Group.objects.get_or_create(name="%s_%d %s" % ("chapter", chapter.id, 'Rush'))
        pending_group = Group.objects.get_or_create(name="%s_%d %s" % ("chapter", chapter.id, 'Pending'))
        chapter.linked_group = group[0]
        chapter.linked_rush_group = rush_group[0]
        chapter.linked_pending_group = pending_group[0]
        chapter.save()


@receiver(signals.post_save, sender=Group)
def set_group_after_group_save(sender, **kwargs):
    if kwargs.get('created'):
        group = kwargs.get('instance')
        if group.name[:7] == 'chapter':
            chapter_id = int(group.name.split(' ')[0].split('_')[1])
            chapter = get_object_or_404(Chapter, id=chapter_id)
            chapter.groups.add(group.id)
            chapter.save()


class Position(Slugged):
    chapter = models.ForeignKey(Chapter)
