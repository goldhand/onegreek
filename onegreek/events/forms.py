from django import forms

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit, Button, Fieldset, HTML

from djangular.forms.angular_model import NgModelFormMixin

from .models import Event


def date_time_widget(ng_model, ng_label):
    return \
    '<div class="form-inline row">' \
    '<div class="span3" style="padding-top: 8px;">' \
    '<label class="control-label">%s</label>' \
    '<div class="controls">' \
    '<input class="span2" type="text" datepicker-popup="yyyy-MM-dd" ng-model="%s" is-open="opened%s" min="minDate" max="\'2015-06-22\'" datepicker-options="dateOptions" ng-required="false" />' \
    '<button class="btn" ng-click="open%s()"><i class="icon-calendar"></i></button>' \
    '</div>' \
    '</div>' \
    '<div class="controls">' \
    '<div ng-model="%s" ng-change="changed()" class="span3">' \
    '<timepicker hour-step="hstep" minute-step="mstep" show-meridian="ismeridian"></timepicker>' \
    '</div>' \
    '</div>' \
    '</div>' \
    % (ng_label, ng_model, ng_label, ng_label, ng_model)

class EventForm(NgModelFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'viewers', 'enable_comments',
            'owner', 'slug',
        ]
        widgets = {
            'owner': forms.HiddenInput(),
            'slug': forms.HiddenInput(),
            #'start': forms.SplitDateTimeWidget(),
            #'end': forms.SplitDateTimeWidget(),
        }


    def __init__(self, *args, **kwargs):
        kwargs.update(scope_prefix='event')
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Div(
                HTML(date_time_widget('event.start', 'Start')),
                HTML(date_time_widget('event.end', 'End')),
                'title',
                'description',
                'viewers',
                'enable_comments'
            )
        )