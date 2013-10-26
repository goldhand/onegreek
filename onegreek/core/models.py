import re
import unicodedata

from django.db import models
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from model_utils.models import TimeStampedModel


class BaseAbstractModel(TimeStampedModel):

    class Meta:
        abstract = True


def base_concrete_model(abstract, instance):
    """
    source: @stephenmcd/mezzanine
    Used in methods of abstract models to find the super-most concrete
    (non abstract) model in the inheritance chain that inherits from the
    given abstract model. This is so the methods in the abstract model can query data consistently across the correct
    concrete model.  Consider the following::

    class Abstract(models.Model)
        class Meta:
            abstract = True
        def concrete(self):
            return base_concrete_model(Abstract, self)

    class Super(Abstract):
        pass

    class Sub(Super):
        pass

    sub = Sub.objects.create()
    sub.concrete()

    # returns Super In actual Mezzanine usage, this allows methods in the ``Displayable`` and ``Orderable`` abstract
    models to access the ``Page`` instance when instances of custom content types, (eg: models that inherit from
    ``Page``) need to query the ``Page`` model to determine correct values for ``slug`` and ``_order`` which are only
    relevant in the context of the ``Page`` model and not the model of the custom content type.
    """

    for cls in reversed(instance.__class__.__mro__):
        if issubclass(cls, abstract) and not cls._meta.abstract:
            return cls
    return instance.__class__


def slugify(s):
    """
    source: @stephenmcd/mezzanine
    """
    chars = []
    for char in unicode(smart_unicode(s)):
        cat = unicodedata.category(char)[0]
        if cat in "LN" or char in "-_~":
            chars.append(char)
        elif cat == "Z":
            chars.append(" ")
    return re.sub("[-\s]+", "-", "".join(chars).strip()).lower()


def unique_slug(queryset, slug_field, slug):
    """
    source: @stephenmcd/mezzanine
    Ensures a slug is unique for the given queryset, appending
    an integer to its end until the slug is unique.
    """
    i = 0
    while True:
        if i > 0:
            if i > 1:
                slug = slug.rsplit("-", 1)[0]
            slug = "%s-%s" % (slug, i)
        try:
            queryset.get(**{slug_field: slug})
        except ObjectDoesNotExist:
            break
        i += 1
    return slug


class Slugged(TimeStampedModel):
    """
    source: @stephenmcd/mezzanine
    Abstract model that handles auto-generating slugs. Each slugged
    object is also affiliated with a specific site object.
    """

    title = models.CharField(_("Title"), max_length=500)
    slug = models.CharField(_("Slug"), max_length=2000, blank=True, null=True,
                            help_text=_("Leave blank to have this auto-generated from the title. (recommended)"))

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Create a unique slug by appending an index.
        """
        if not self.slug:
            self.slug = self.get_slug()
        concrete_model = base_concrete_model(Slugged, self)
        slug_qs = concrete_model.objects.exclude(id=self.id)
        self.slug = unique_slug(slug_qs, "slug", self.slug)
        super(Slugged, self).save(*args, **kwargs)

    def get_slug(self):
        """
        Allows subclasses to implement their own slug creation logic.
        """
        return slugify(self.title)

    def admin_link(self):
        return "<a href='%s'>%s</a>" % (self.get_absolute_url(),
                                        ugettext("View on site"))

    admin_link.allow_tags = True
    admin_link.short_description = ""


