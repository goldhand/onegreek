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

from phonenumber_field.modelfields import PhoneNumberField


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
            ('rush', _('Rushee')),
        ]),
        ('Pledge', [
            ('pledge', _('Pledge')),
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
    )
    PROFILE_IMG_OPTIONS = (
        (0, 'Facebook Default'),
        (1, 'Facebook Album'),
        (2, 'Upload New'),
    )

    university_email = models.EmailField(max_length=255, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    highschool_gpa = models.DecimalField(null=True, blank=True, max_digits=3, decimal_places=2)
    gpa = models.DecimalField(null=True, blank=True, max_digits=3, decimal_places=2)
    year = models.IntegerField(choices=COLLEGE_YEARS, default=0)
    major = models.CharField(max_length=255, blank=True)
    hometown = models.CharField(max_length=255, blank=True)
    chapter = models.ForeignKey('chapters.Chapter', blank=True, null=True,
                                help_text="Select your chapter " \
                                          "*note: your membership will be pending until it is approved by " \
                                          "your chapter's administrator")
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

    def get_fb_extra_data(self):
        u_social = self.socialaccount_set.all()
        if u_social:
            return u_social[0].extra_data

    @property
    def fb_uid(self):
        fb_uid = SocialAccount.objects.filter(user_id=self.id, provider='facebook')

        if len(fb_uid):
            return fb_uid[0].uid
        else:
            return None

    def is_chapter_admin(self):
        if self.chapter:
            return self in self.chapter.linked_admin_group.user_set.all()
        else:
            return False

    def get_attending(self):
        return self.attending.filter(active=True)

    def get_rsvps(self):
        return self.rsvps.filter(active=True)

    @property
    def name(self):
        return self.get_full_name()

    def get_api_url(self):
        return "/users/~#/users/%d" % self.id

    @property
    def profile_complete(self):
        if self.status == 'rush':
            if self.first_name and self.last_name and self.phone and self.hometown:
                if self.gpa or self.highschool_gpa:
                    return True
            return False
        else:
            return True


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


from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added
from allauth.socialaccount.models import SocialAccount
import urllib2, urllib


@receiver(user_signed_up, dispatch_uid="some.unique.string.id.for.allauth.user_signed_up")
def post_to_facebook(request, user, **kwargs):
    post_url = "https://graph.facebook.com/{}/".format(user.fb_uid)
    post_data = [("message", "{} {}".format(user.get_full_name(), 'has joined Onegreek')), ('access_token', user.get_fb_access_token().token)]
    print urllib.urlencode(post_data)
    print post_url
    urllib2.urlopen(post_url, urllib.urlencode(post_data))


