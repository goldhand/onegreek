from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver

from model_utils.fields import SplitField, StatusField
from model_utils.models import StatusModel
from model_utils import Choices, FieldTracker

from core.models import Slugged, base_concrete_model, unique_slug
from django.db.models import signals


class Chapter(Slugged, StatusModel):

    STATUS = Choices('excellence', 'achievement', 'probation', 'inactive')
    fraternity = models.ForeignKey('fraternities.Fraternity', null=True, blank=True)
    university = models.ForeignKey('universities.University', null=True, blank=True)
    description = SplitField(blank=True)
    #location = models.TextField(blank=True)
    awards = SplitField(blank=True)
    philanthropy = SplitField(blank=True)
    potential_new_members = SplitField(blank=True)
    facebook = models.URLField(blank=True)
    fb_status = models.TextField(blank=True)
    cost = models.IntegerField(blank=True, null=True)
    gpa = models.FloatField(blank=True, null=True)
    groups = models.ManyToManyField(Group, null=True, blank=True)
    linked_group = models.OneToOneField(Group, null=True, blank=True, related_name='linked_chapter')

    _tracker = FieldTracker()

    class Meta:
        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"
        permissions = (
            ('view_chapter', 'view_chapter'),
        )

    def get_absolute_url(self):
        return reverse('chapters:detail', kwargs={'pk': self.pk})



@receiver(signals.post_save, sender=Chapter)
def set_group(sender, **kwargs):
    chapter = kwargs.get('instance')
    if not chapter.linked_group:
        group = Group.objects.get_or_create(name="%s_%d" % ("chapter", chapter.id))
        chapter.linked_group = group[0]
        chapter.save()


