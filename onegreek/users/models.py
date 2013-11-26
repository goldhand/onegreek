# -*- coding: utf-8 -*-
# Import the AbstractUser model
from django.contrib.auth.models import AbstractUser, Group
from django.contrib import messages

# Import the basic Django ORM models library
from django.db import models
from django.db.models import signals
from django.dispatch import receiver

from allauth.socialaccount.models import SocialAccount
import hashlib

from django.utils.translation import ugettext_lazy as _
from model_utils import Choices, FieldTracker
from model_utils.models import StatusModel


class User(AbstractUser, StatusModel):
    STATUS = Choices(
        ('Rushing', [
            ('rushing', _('Rushing')),
        ]),
        ('Pledging', [
            ('pledging', _('Pledging')),
            ('pledge_dropped', _('Dropped from Pledge'))
        ]),
        ('Active', [
            ('active', _('Active')),
            ('alumni', _('Alumni')),
            ('pending', _('Pending Active')),
            ('active_dropped', _('Withdrew from Chapter')),
        ]),
        ('guest', _('Guest')),
    )
    COLLEGE_YEARS = (
        (0, 'Freshman'),
        (1, 'Sophomore'),
        (2, 'Junior'),
        (3, 'Senior'),
        (4, 'Other'),
    )

    university_email = models.EmailField(max_length=255, blank=True)
    phone = models.BigIntegerField(null=True, blank=True)
    highschool_gpa = models.FloatField(null=True, blank=True)
    gpa = models.FloatField(null=True, blank=True)
    year = models.IntegerField(choices=COLLEGE_YEARS, default=0)
    major = models.CharField(max_length=255, blank=True)
    hometown = models.CharField(max_length=255, blank=True)
    chapter = models.ForeignKey('chapters.Chapter', blank=True, null=True,
                                help_text="Leave blank to continue as a rushee")
    university = models.ForeignKey('universities.University', blank=True, null=True)
    fraternity = models.ForeignKey('fraternities.Fraternity', blank=True, null=True)
    position = models.ForeignKey('chapters.Position', blank=True, null=True)

    _tracker = FieldTracker()

    def __unicode__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.chapter_id:
            self.university = self.chapter.university
            self.fraternity = self.chapter.fraternity

        return super(User, self).save(*args, **kwargs)

    def profile_image_url(self):
        fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')

        if len(fb_uid):
            return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)

        return "http://www.gravatar.com/avatar/{}?s=40".format(hashlib.md5(self.user.email).hexdigest())




@receiver(signals.post_save, sender=User)
def set_new_user_config(sender, **kwargs):
    user = kwargs.get('instance')
    if kwargs.get('created'):
        user_msg = ""
        # New user?
        user_msg = "Signed up as %s %s, %s" % (user.first_name, user.last_name, user.status)
        # Is he a pending active?
        if user.chapter_id:
            group_id = user.chapter.linked_pending_group_id
            user.groups.add(group_id)
            user.status = "pending"
        else:
            user.status = "rushing"
        user.save()
    else:
        if user.status == "rushing" and user.chapter_id:
            group_id = user.chapter.linked_pending_group_id
            user.groups.add(group_id)
            user.status = "pending"
            user.save()
        elif user.status == "pending" and not user.chapter_id:
            user.status = "rushing"
            user.groups = []
            user.fraternity = None
            user.save()



        #class UserPosition(models.Model):

        # home page
        #register
        #active
        #added to "pending actives" group
        #rushee
        #fills out custom form for rushing chapter



#check in users

