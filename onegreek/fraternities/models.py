from django.db import models

from django.db import models
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
    group = models.ForeignKey(Group, null=True, blank=True)

    _tracker = FieldTracker()

    class Meta:
        verbose_name = "Fraternity"
        verbose_name_plural = "Fraternities"

    def save(self, *args, **kwargs):
        """
        Create a unique slug by appending an index.
        """
        if not self.slug:
            self.slug = self.get_slug()
        concrete_model = base_concrete_model(Slugged, self)
        slug_qs = concrete_model.objects.exclude(id=self.id)
        self.slug = unique_slug(slug_qs, "slug", self.slug)

        try:
            self.group = Group.objects.get(name="%s_%s" % ("fraternity", self.slug))
        except ObjectDoesNotExist:
            self.group = Group.objects.create(name="%s_%s" % ("fraternity", self.slug))

        super(Fraternity, self).save(*args, **kwargs)
