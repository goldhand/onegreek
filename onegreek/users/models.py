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


def color_key(status, component=None):
    if status == "active":
        _class = "error"
        if component == "btn":
            _class = "danger"
    elif status == "pledge":
        _class = "success"
    elif status == "rush":
        _class = "info"
    elif status == "active":
        _class = "warning"
    elif status == "active_pending":
        _class = "muted"
    else:
        _class = ""
    if component == "table":
        return _class
    else:
        return "%s-%s" % (component, _class)


def get_status_text_class(self):
    return color_key(self.status, "text")



class User(AbstractUser, StatusModel):
    STATUS = Choices(
        ('Rushing', [
            ('rush', _('Rushing')),
        ]),
        ('Pledge', [
            ('pledge', _('Pledging')),
            ('pledge_dropped', _('Dropped from Pledge'))
        ]),
        ('Active', [
            ('active', _('Active')),
            ('alumni', _('Alumni')),
            ('active_pending', _('Active Pending')),
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
    PROFILE_IMG_OPTIONS = (
        (0, 'Facebook Default'),
        (1, 'Facebook Album'),
        (2, 'Upload New'),
    )

    university_email = models.EmailField(max_length=255, blank=True)
    phone = models.BigIntegerField(null=True, blank=True)
    highschool_gpa = models.FloatField(null=True, blank=True)
    gpa = models.FloatField(null=True, blank=True)
    year = models.IntegerField(choices=COLLEGE_YEARS, default=0)
    major = models.CharField(max_length=255, blank=True)
    hometown = models.CharField(max_length=255, blank=True)
    chapter = models.ForeignKey('chapters.Chapter', blank=True, null=True,
                                help_text="Select your chapter " \
                                          "*note: your active status will be pending until approved by an administrator")
    university = models.ForeignKey('universities.University', blank=True, null=True)
    fraternity = models.ForeignKey('fraternities.Fraternity', blank=True, null=True)
    position = models.ForeignKey('chapters.Position', blank=True, null=True)
    profile_img_id = models.CharField(max_length=500, blank=True)
    profile_img_src = models.URLField(max_length=500, blank=True)
    profile_img_pic = models.URLField(max_length=500, blank=True)
    profile_img_select = models.IntegerField(choices=PROFILE_IMG_OPTIONS, default=0)

    _tracker = FieldTracker()

    def __unicode__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.chapter_id:
            self.university = self.chapter.university
            self.fraternity = self.chapter.fraternity

        return super(User, self).save(*args, **kwargs)

    def profile_image_url(self):

        if self.profile_img_select == 0:
            fb_uid = SocialAccount.objects.filter(user_id=self.id, provider='facebook')
            if len(fb_uid):
                return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)
            else:
                if self.avatar_set.all():
                    avatar = self.avatar_set.filter(primary=True)[0]
                    return avatar.avatar_url(80)
                else:
                    return "http://www.gravatar.com/avatar/{}?s=40".format(hashlib.md5(self.email).hexdigest())

        elif self.profile_img_select == 1:
            if self.profile_img_pic:
                return self.profile_img_pic
            else:
                fb_uid = SocialAccount.objects.filter(user_id=self.id, provider='facebook')
                if len(fb_uid):
                    return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)
        else:
            if self.avatar_set.all():
                avatar = self.avatar_set.filter(primary=True)[0]
                return avatar.avatar_url(80)
            else:
                return "http://www.gravatar.com/avatar/{}?s=40".format(hashlib.md5(self.email).hexdigest())

    def profile_image_lg_url(self):
        if self.profile_img_select == 0:
            fb_uid = SocialAccount.objects.filter(user_id=self.id, provider='facebook')
            if len(fb_uid):
                return "http://graph.facebook.com/{}/picture?width=300&height=300".format(fb_uid[0].uid)
            if self.avatar_set.all():
                avatar = self.avatar_set.filter(primary=True)
                if avatar:
                    return avatar[0].avatar_url(300)
            else:
                return "http://www.gravatar.com/avatar/{}?s=300".format(hashlib.md5(self.email).hexdigest())

        elif self.profile_img_select == 1:
            if self.profile_img_src:
                return self.profile_img_src
            else:
                fb_uid = SocialAccount.objects.filter(user_id=self.id, provider='facebook')
                if len(fb_uid):
                    return "http://graph.facebook.com/{}/picture?width=300&height=300".format(fb_uid[0].uid)
        else:
            if self.avatar_set.all():
                avatar = self.avatar_set.filter(primary=True)
                if avatar:
                    return avatar[0].avatar_url(300)
            else:
                return "http://www.gravatar.com/avatar/{}?s=300".format(hashlib.md5(self.email).hexdigest())

    def fb_photos(self):
        fb_uid = SocialAccount.objects.filter(user_id=self.id, provider='facebook')

        if len(fb_uid):
            return "https://graph.facebook.com/{}/?fields=albums".format(fb_uid[0].uid)

    def get_fb_access_token(self):
        fb_uid = SocialAccount.objects.filter(user_id=self.id, provider='facebook')
        if fb_uid:
            return fb_uid[0].socialtoken_set.all()[0]


    def is_chapter_admin(self):
        if self.chapter:
            return self in self.chapter.linked_admin_group.user_set.all()
        else:
            return False

    def get_attending(self):
        return self.attending.filter(active=True)

    def get_rsvps(self):
        return self.rsvps.filter(active=True)


@receiver(signals.post_save, sender=User)
def set_new_user_config(sender, **kwargs):
    user = kwargs.get('instance')
    if kwargs.get('created'):
        # Is he a pending active?
        if user.chapter_id:
            group_id = user.chapter.linked_pending_group_id
            user.groups.add(group_id)
            user.status = "active_pending"
        else:
            user.status = "rush"
        user.save()
    else:
        # Was a pending active but changed to rushee
        if user.status == "active_pending" and not user.chapter_id:
            user.status = "rush"
            user.groups.clear()
            user.fraternity = None
            user.save()
        # Was a rushee but changed to pending active
        elif user.status == "rush" and user.chapter_id:
            user.groups.clear()
            pending_group_id = user.chapter.linked_pending_group_id
            user.groups.add(pending_group_id)
            user.status = "active_pending"
            user.save()


import re


@receiver(signals.post_save, sender=Group)
def set_group_and_status(sender, **kwargs):
    if not kwargs['created']:
        group = kwargs.get('instance')
        if re.match("chapter_.+? Active", str(group.name)):
            chapter = group.linked_chapter_active
            for user in group.user_set.all():
                if not user.status == "active":
                    user.status = "active"
                    if not user.chapter == chapter:
                        user.chapter = chapter
                    user.groups.clear()
                    user.groups.add(group, chapter.linked_group)
                    user.save()
        elif re.match("chapter_.+? Pledge", str(group.name)):
            chapter = group.linked_chapter_pledge
            for user in group.user_set.all():
                if not user.status == "pledge":
                    user.status = "pledge"
                    if not user.chapter == chapter:
                        user.chapter = chapter
                    user.groups.clear()
                    user.groups.add(group, chapter.linked_group)
                    user.save()
        if re.match("chapter_.+? Pending", str(group.name)):
            chapter = group.linked_chapter_pending
            for user in group.user_set.all():
                if not user.status == "active_pending":
                    user.status = "active_pending"
                    if not user.chapter == chapter:
                        user.chapter = chapter
                    user.groups.clear()
                    user.groups.add(group)
                    user.save()
        elif re.match("chapter_.+? Rush", str(group.name)):
            for user in group.user_set.all():
                if not user.status == "rush":
                    user.status = "rush"
                    if user.chapter:
                        user.chapter = None
                    user.groups.clear()
                    user.groups.add(group)
                    user.save()


