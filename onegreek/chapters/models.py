from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import signals
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from guardian.shortcuts import assign_perm, get_perms

from model_utils.fields import SplitField, StatusField
from model_utils.models import StatusModel
from model_utils import Choices, FieldTracker

from core.models import Slugged, base_concrete_model, unique_slug
from rush_forms.models import Form, Field


class Chapter(Slugged, StatusModel):
    STATUS = Choices('excellence', 'achievement', 'probation', 'inactive')
    fraternity = models.ForeignKey('fraternities.Fraternity', null=True, blank=True)
    university = models.ForeignKey('universities.University', null=True, blank=True)
    fraternity_title = models.CharField(max_length=255, blank=True,
                                        help_text='Leave blank to have this field auto-populated')
    university_title = models.CharField(max_length=255, blank=True,
                                        help_text='Leave blank to have this field auto-populated')
    description = SplitField(blank=True)
    location = models.TextField(blank=True)
    awards = SplitField(blank=True)
    philanthropy = SplitField(blank=True)
    potential_new_members = SplitField(blank=True)
    facebook = models.URLField(blank=True)
    fb_status = models.TextField(blank=True)
    cost = models.IntegerField(blank=True, null=True)
    gpa = models.FloatField(blank=True, null=True)
    groups = models.ManyToManyField(Group, null=True, blank=True,
                                    help_text='Leave blank to have this field auto-populated')
    linked_group = models.OneToOneField(Group, null=True, blank=True, related_name='linked_chapter',
                                        help_text='Leave blank to have this field auto-populated')
    linked_rush_group = models.OneToOneField(Group, null=True, blank=True, related_name='linked_chapter_rush',
                                             help_text='Leave blank to have this field auto-populated')
    linked_call_group = models.OneToOneField(Group, null=True, blank=True, related_name='linked_chapter_call',
                                                  help_text='Leave blank to have this field auto-populated')
    linked_pledge_group = models.OneToOneField(Group, null=True, blank=True, related_name='linked_chapter_pledge',
                                               help_text='Leave blank to have this field auto-populated')
    linked_pending_group = models.OneToOneField(Group, null=True, blank=True, related_name='linked_chapter_pending',
                                                help_text='Leave blank to have this field auto-populated')
    linked_active_group = models.OneToOneField(Group, null=True, blank=True, related_name='linked_chapter_active',
                                               help_text='Leave blank to have this field auto-populated')
    linked_admin_group = models.OneToOneField(Group, null=True, blank=True, related_name='linked_chapter_admin',
                                              help_text='Leave blank to have this field auto-populated')
    rush_form = models.OneToOneField('rush_forms.Form', null=True, blank=True, related_name="chapter",
                                     help_text='Leave blank to have this field auto-populated')

    _tracker = FieldTracker()

    class Meta:
        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"
        permissions = (
            ('view_chapter', 'view_chapter'),
        )

    def __unicode__(self):
        if self.fraternity and self.university:
            return "%s - %s " % (self.fraternity.title, self.university.title)
        else:
            return self.title

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
        if not self.groups.count <= 6:
            self.groups.add(self.linked_group)
            self.groups.add(self.linked_rush_group)
            self.groups.add(self.linked_call_group)
            self.groups.add(self.linked_pledge_group)
            self.groups.add(self.linked_pending_group)
            self.groups.add(self.linked_active_group)
            self.groups.add(self.linked_admin_group)
        return self.groups.all()

    def get_content_type_id(self):
        return ContentType.objects.get_for_model(self).id


@receiver(signals.post_save, sender=Chapter)
def set_group(sender, **kwargs):
    if kwargs.get('created'):
        chapter = kwargs.get('instance')

        # create dict of all chapter groups, get or create the groups
        cg_set = {
            'group': Group.objects.get_or_create(name="%s_%d %s" % ("chapter", chapter.id, chapter.title))[0],
            'rush_group': Group.objects.get_or_create(name="%s_%d %s" % ("chapter", chapter.id, 'Rush'))[0],
            'call_group': Group.objects.get_or_create(name="%s_%d %s" % ("chapter", chapter.id, 'Call List'))[0],
            'pledge_group': Group.objects.get_or_create(name="%s_%d %s" % ("chapter", chapter.id, 'Pledge'))[0],
            'pending_group': Group.objects.get_or_create(name="%s_%d %s" % ("chapter", chapter.id, 'Pending'))[0],
            'active_group': Group.objects.get_or_create(name="%s_%d %s" % ("chapter", chapter.id, 'Active'))[0],
            'admin_group': Group.objects.get_or_create(name="%s_%d %s" % ("chapter", chapter.id, 'Admin'))[0],
        }

        # give permissions to each group
        for k, v in cg_set.items():
            # assign to all groups
            assign_perm('chapters.view_chapter', v)
            assign_perm('events.view_event', v)
            assign_perm('rest_comments.view_restcomment', v)
            assign_perm('rush_forms.view_form', v)
            if k == 'admin_group':
                assign_perm('chapters.change_chapter', v, chapter)
                assign_perm('events.add_event', v)
                assign_perm('events.delete_event', v)
                assign_perm('events.change_event', v)
                assign_perm('rush_forms.change_form', v)
                assign_perm('rest_comments.add_restcomment', v)
                assign_perm('rest_comments.change_restcomment', v)
                assign_perm('rest_comments.delete_restcomment', v)
            elif k == 'active_group':
                assign_perm('rest_comments.add_restcomment', v)
                assign_perm('rest_comments.change_restcomment', v)
                assign_perm('rest_comments.delete_restcomment', v)


        # assign groups from cg_set to chapter
        chapter.linked_group = cg_set['group']
        chapter.linked_rush_group = cg_set['rush_group']
        chapter.linked_call_group = cg_set['call_group']
        chapter.linked_pledge_group = cg_set['pledge_group']
        chapter.linked_pending_group = cg_set['pending_group']
        chapter.linked_active_group = cg_set['active_group']
        chapter.linked_admin_group = cg_set['admin_group']

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
