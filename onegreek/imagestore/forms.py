#!/usr/bin/env python
# vim:fileencoding=utf-8
try:
    import autocomplete_light
    AUTOCOMPLETE_LIGHT_INSTALLED = True
except ImportError:
    AUTOCOMPLETE_LIGHT_INSTALLED = False

__author__ = 'zeus'

from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit, Button, Fieldset, HTML

from models import Image, Album


class ImageForm(forms.ModelForm):
    class Meta(object):
        model = Image
        exclude = ('user', 'order', 'status_changed',
                   )
        widgets = {
            'status': forms.HiddenInput(),
        }

    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 19}), required=False,
                                  label=_('Description'))
    #content_type = forms.CharField(widget=forms.HiddenInput())
    #object_pk = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, user, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['album'].queryset = Album.objects.filter(user=user)
        self.fields['album'].required = True
        if AUTOCOMPLETE_LIGHT_INSTALLED:
            self.fields['tags'].widget = autocomplete_light.TextWidget('TagAutocomplete')


class ImageFormCrispy(forms.ModelForm):
    class Meta(object):
        model = Image
        exclude = ('user', 'order', 'status_changed',
                   )
        fields = ['image', 'album', 'content_type', 'object_pk', 'status']
        widgets = {
            'status': forms.HiddenInput(),
            'content_type': forms.HiddenInput(),
            'object_pk': forms.HiddenInput(),

            }
    #content_type = forms.CharField(widget=forms.HiddenInput())
    #object_pk = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, user, content_type=None, object_pk=None, *args, **kwargs):
        super(ImageFormCrispy, self).__init__(*args, **kwargs)
        self.fields['album'].queryset = Album.objects.filter(user=user)
        self.fields['album'].required = True
        self.fields['status'].initial = 'public'
        if content_type:
            self.fields['content_type'].initial = content_type
        if object_pk:
            self.fields['object_pk'].initial = object_pk
        if AUTOCOMPLETE_LIGHT_INSTALLED:
            self.fields['tags'].widget = autocomplete_light.TextWidget('TagAutocomplete')
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.form_action = 'imagestore:upload'
        self.helper.add_input(Submit('submit', 'Submit'))


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

