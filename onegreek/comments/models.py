from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group

from model_utils.fields import SplitField, StatusField
from model_utils.models import StatusModel
from model_utils import Choices, FieldTracker
from model_utils.models import TimeStampedModel

from rest_framework.renderers import JSONRenderer

from guardian.shortcuts import assign_perm

from core.models import Slugged

from django.contrib import comments


class PComment(comments.Comment):
    """
    Comment with viewers
    """
    viewers = models.ManyToManyField('chapters.Chapter', null=True, blank=True)

    class Meta:
        permissions = (
            ('view_comment', 'View Comment'),
            ('change_comment', 'Edit Comment'),
            ('delete_comment', 'Delete Comment'),
        )
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def save(self, *args, **kwargs):
        """
        Assign permissions but also use default behavior
        """
        if self.submit_date is None:
            self.submit_date = timezone.now()

        super(PComment, self).save(*args, **kwargs)

        #assign_perm('change_comment', self.user, self)
        assign_perm('view_comment', Group.objects.get(name="chapter_%d" % self.user.chapter_id), self)

        viewers = self.viewers.all()
        if viewers:
            for viewer in viewers:
                assign_perm('view_comment', Group.objects.get(name="chapter_%d" % viewer.id), self)

    def __unicode__(self):
        if self.object_pk:
            return "%d_%s-%d" % (self.user_id, self.content_type, self.object_pk)
        else:
            return "%d_%s-%d" % (self.user_id, 'none', 0)

    def user_can_view(self, _user):
        if _user.chapter in self.viewers.all() or self.user == _user:
            return True
        else:
            return False
