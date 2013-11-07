from django import forms

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit, Button, Fieldset, HTML

from djangular.forms.angular_model import NgModelFormMixin

from .models import Event


class EventForm(NgModelFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        widgets = {
            'owner': forms.HiddenInput(),
            'slug': forms.HiddenInput(),
            #'start': forms.SplitDateTimeWidget(),
            #'end': forms.SplitDateTimeWidget(),
        }


    def __init__(self, *args, **kwargs):
        kwargs.update(scope_prefix='events')
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        #self.helper.layout = Layout(
        #    Fieldset(