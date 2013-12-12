from django import forms
try:
    import autocomplete_light
    AUTOCOMPLETE_LIGHT_INSTALLED = True
except ImportError:
    AUTOCOMPLETE_LIGHT_INSTALLED = False

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Image, Album


class ImageForm(forms.ModelForm):
    class Meta(object):
        model = Image
        exclude = ('user', 'order', 'status_changed')

    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 19}), required=False,
                                  label=_('Description'))

    def __init__(self, user, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['album'].queryset = Album.objects.filter(user=user)
        self.fields['album'].required = True
        if AUTOCOMPLETE_LIGHT_INSTALLED:
            self.fields['tags'].widget = autocomplete_light.TextWidget('TagAutocomplete')


class AlbumForm(forms.ModelForm):
    class Meta(object):
        model = Album
        exclude = ('user', 'created', 'updated')

    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            self.fields['head'].queryset = Image.objects.filter(album=kwargs['instance'])
        else:
            self.fields['head'].widget = forms.HiddenInput()
