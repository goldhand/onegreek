from django.db import models
from guardian.shortcuts import assign_perm, get_perms
from django.db.models import signals
from django.dispatch import receiver

from django_comments.models import Comment
from django_comments.signals import comment_was_posted


class RestComment(Comment):
    class Meta:
        verbose_name = "Rest Comment"
        verbose_name_plural = "Rest Comments"
        permissions = (
            ('view_restcomment', 'view_restcomment'),
        )


@receiver(comment_was_posted, sender=RestComment)
def set_group(sender, **kwargs):
    comment = kwargs.get('instance')
    request = kwargs.get('request')
    #chapter_group = comment.user.chapter.linked_group

    #if chapter_group:
    #    assign_perm('view_restcomment', chapter_group, comment)
    if 'viewers' in request.POST:
        viewers = request.POST['viewers']
        print viewers
