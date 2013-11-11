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
    groups = models.ManyToManyField(Group, null=True, blank=True)

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


        return super(Chapter, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('chapters:detail', kwargs={'pk': self.pk})



'''
        if not self.groups.all():
            group_qs = Group.objects.all()
            group_name = "chapter_" + str(self.slug)
            group_name = unique_slug(group_qs, "name", group_name)
            group = Group.objects.create(group_name)
            self.groups.add(group.id)

@receiver(signals.post_save, sender=Chapter)
def set_group(sender, **kwargs):
    chapter = kwargs.get('instance')
    print chapter.title
    if not chapter.groups.all():
        try:
            group = Group.objects.get(name="chapter" + str(chapter.id))
        except ObjectDoesNotExist:
            group = Group.objects.create(name="chapter" + str(chapter.id))
        chapter.groups.add(group)
        chapter.save()
        print(chapter.groups.all())
    else:
        pass
'''
