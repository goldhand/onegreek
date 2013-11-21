# -*- coding: utf-8 -*-
# Import the AbstractUser model
from django.contrib.auth.models import AbstractUser, Group

# Import the basic Django ORM models library
from django.db import models
from django.db.models import signals
from django.dispatch import receiver

from django.utils.translation import ugettext_lazy as _
from model_utils import Choices


# Subclass AbstractUser
class User(AbstractUser):
    STATUS = Choices(
        ('guest', 'Guest'),
        ('Potential', ['guest', 'rushee']),
        ('Active', [
            ('goodstanding', 'In Good Standing'),
            ('badstanding', 'In Bad Standing'),
            ('alumni', 'Alumni'),
            ('pledge', 'Pledge'),
        ]),
        ('Inactive', [
            ('withdrew', 'Withdrew'),
            ('unaccepted', 'Did not pass Pledging')
        ])
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
    chapter = models.ForeignKey('chapters.Chapter', blank=True, null=True)
    university = models.ForeignKey('universities.University', blank=True, null=True)
    fraternity = models.ForeignKey('fraternities.Fraternity', blank=True, null=True)
    position = models.ForeignKey('chapters.Position', blank=True, null=True)

    def __unicode__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.chapter:
            self.university = self.chapter.university
            self.fraternity = self.chapter.fraternity

        return super(User, self).save(*args, **kwargs)


#class UserPosition(models.Model):

# home page
        #register
            #active
                #added to "pending actives" group
            #rushee
                #fills out custom form for rushing chapter



#check in users
#