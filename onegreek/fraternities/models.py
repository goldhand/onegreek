from django.db import models

from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist

from model_utils.fields import SplitField, StatusField
from model_utils.models import StatusModel
from model_utils import Choices, FieldTracker

from core.models import Slugged, base_concrete_model, unique_slug


class Fraternity(Slugged):

    description = SplitField()
    facebook = models.URLField(blank=True)
    fb_status = models.TextField(blank=True)
    gpa = models.FloatField()
    group = models.OneToOneField(Group, null=True, blank=True)

    _tracker = FieldTracker()

    class Meta:
        verbose_name = "Fraternity"
        verbose_name_plural = "Fraternities"


@receiver(signals.post_save, sender=Fraternity)
def set_group(sender, **kwargs):
    fraternity = kwargs.get('instance')
    if not fraternity.group:
        group = Group.objects.get_or_create(name="%s_%d" % ("fraternity", fraternity.id))
        fraternity.group = group[0]
        fraternity.save()
