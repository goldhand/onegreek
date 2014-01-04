from django.core.urlresolvers import reverse
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from model_utils import Choices

from model_utils.models import StatusModel

from bases.album import BaseAlbum
from imagestore.utils import load_class, get_model_string


class Album(BaseAlbum, StatusModel):
    STATUS = Choices(
        ('draft', 'Draft'),
        ('public', 'Public'),
        ('chapter', 'Your Chapter'),
        ('rush', 'Rushes'),
        ('pledge', 'Pledges'),
        ('active', 'Actives')
    )
    content_type = models.ForeignKey(ContentType,
                                     verbose_name=_('content type'),
                                     related_name="content_type_set_for_%(class)s")
    object_pk = models.TextField(_('object ID'))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    class Meta(BaseAlbum.Meta):
        abstract = False
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')
        app_label = 'imagestore'


from chapters.models import Chapter
@receiver(models.signals.post_save, sender=Chapter)
def set_group(sender, **kwargs):
    if kwargs.get('created'):
        chapter = kwargs.get('instance')
        print chapter.title
        Album.objects.create(status="public",
                             content_type=ContentType.objects.get_for_model(chapter),
                             object_pk=str(chapter.pk),
                             is_public=True,
                             name='Event Images')
