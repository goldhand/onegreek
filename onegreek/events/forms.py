from django import forms

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit, Button, Fieldset, HTML

from djangular.forms.angular_model import NgModelFormMixin

from .models import Event
from .widgets import BootstrapDateTimeInput


def date_time_widget(ng_model, ng_label):
    return \
        '<div class="form-inline row">' \
        '<div class="span3" style="padding-top: 8px;">' \
        '<label class="control-label">%s</label>' \
        '<div class="controls">' \
        '<input class="span3" type="text" datepicker-popup="yyyy-MM-dd" ng-model="%s" is-open="opened%s" min="minDate" max="\'2015-06-22\'" datepicker-options="dateOptions" ng-required="false" />' \
        '</div>' \
        '</div>' \
        '<div class="controls">' \
        '<div ng-model="%s" ng-change="changed()" class="time-picker-widget">' \
        '<timepicker hour-step="hstep" minute-step="mstep" show-meridian="ismeridian"></timepicker>' \
        '</div>' \
        '</div>' \
        '</div>' \
        % (ng_label, ng_model, ng_label, ng_model)


def status_widget():
    return \
        '<div class="btn-group">' \
        '<button type="button" class="btn btn-primary" ng-model="event.status" btn-radio="\'rush\'">Rush</button>' \
        '<button type="button" class="btn btn-primary" ng-model="event.status" btn-radio="\'call\'">Call</button>' \
        '<button type="button" class="btn btn-primary" ng-model="event.status" btn-radio="\'pledge\'">Pledge</button>' \
        '<button type="button" class="btn btn-primary" ng-model="event.status" btn-radio="\'active\'">Active</button>' \
        '<button type="button" class="btn btn-primary" ng-model="event.status" btn-radio="\'public\'">Public</button>' \
        '</div>'


class EventForm(NgModelFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'enable_comments',
            'owner', 'slug'
        ]
        widgets = {
            'owner': forms.HiddenInput(),
            'slug': forms.HiddenInput(),
            'enable_comments': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        kwargs.update(scope_prefix='event')
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Div(
                Div(
                    HTML(date_time_widget('event.start', 'Start')),
                    HTML(date_time_widget('event.end', 'End')),
                    Field('title', css_class="input-block-level"),
                    HTML(status_widget()),
                    css_class="span6"
                ),
                Div(
                    Field('description', css_class="input-block-level"),
                    css_class="span6"
                ),
                css_class="row"

            )
        )


class EventFormFlat(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'enable_comments',
            'owner', 'slug', 'start', 'end', 'status'
        ]
        exclude = ('status',)
        widgets = {
            'owner': forms.HiddenInput(),
            'slug': forms.HiddenInput(),
            'enable_comments': forms.HiddenInput(),
            'start': BootstrapDateTimeInput(),
            'end': BootstrapDateTimeInput(),
        }

    def __init__(self, *args, **kwargs):
        super(EventFormFlat, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(
                'title'
                'description',
            ),
            Div(
                'start',
                'end',
            )
            )
        )
