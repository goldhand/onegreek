from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist

from model_utils.fields import SplitField, StatusField
from model_utils.models import StatusModel
from model_utils import Choices, FieldTracker

from core.models import Slugged, base_concrete_model, unique_slug


#TODO: Need to send a signal when fraternity or university fields update. Equivalent user fields should update when siganled
class Chapter(Slugged, StatusModel):

    STATUS = Choices('excellence', 'achievement', 'probation', 'inactive')
    fraternity = models.ForeignKey('fraternities.Fraternity', null=True, blank=True)
    university = models.ForeignKey('universities.University', null=True, blank=True)
    description = SplitField()
    awards = SplitField()
    philanthropy = SplitField()
    potential_new_members = SplitField()
    facebook = models.URLField(blank=True)
    fb_status = models.TextField(blank=True)
    cost = models.IntegerField()
    gpa = models.FloatField()
    group = models.ForeignKey(Group, null=True, blank=True)

    _tracker = FieldTracker()

    def save(self, *args, **kwargs):
        """
        Create a unique slug by appending an index.
        """
        if not self.slug:
            self.slug = self.get_slug()
        concrete_model = base_concrete_model(Slugged, self)
        slug_qs = concrete_model.objects.exclude(id=self.id)
        self.slug = unique_slug(slug_qs, "slug", self.slug)

        super(Chapter, self).save(*args, **kwargs)
        try:
            self.group = Group.objects.get(name="%s_%d" % ("chapter", self.pk))
        except ObjectDoesNotExist:
            self.group = Group.objects.create(name="%s_%d" % ("chapter", self.pk))
        super(Chapter, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('chapters:detail', kwargs={'pk': self.pk})


