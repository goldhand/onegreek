from django import forms

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit, Button, Fieldset, HTML

from djangular.forms.angular_model import NgModelFormMixin

from .models import Chapter



class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = [
            'title',
            'university',
            'fraternity',
            'description',
            'cost',
            'chapter_website',
            'founding_year',
            'chapter_address',
            'awards',
            'philanthropy',
            'potential_new_members',
            ]

    def __init__(self, *args, **kwargs):
        #kwargs.update(scope_prefix='event')
        super(ChapterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        #self.helper.form_action = '.'
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('title', css_class="input-block-level"),
                    Field('fraternity', css_class="input-block-level"),
                    Field('university', css_class="input-block-level"),
                    Field('chapter_website', css_class="input-block-level"),
                    Field('founding_year', css_class="input-block-level"),
                    Field('cost', css_class="input-block-level"),
                    Field('description', css_class="input-block-level", rows='4'),
                    css_class="span6"
                ),
                Div(
                    Field('chapter_address', css_class="input-block-level", rows='4'),
                    Field('awards', css_class="input-block-level", rows='4'),
                    Field('philanthropy', css_class="input-block-level", rows='4'),
                    Field('potential_new_members', css_class="input-block-level", rows='4'),
                    css_class="span6"
                ),
                css_class='row',
            ),
            FormActions(
                Div(
                    Submit('submit', 'Submit', css_class="btn btn-primary btn-large"),
                    HTML('<a href="/chapters/" class="btn btn-default btn-large">Cancel</a>'),
                    css_class="btn-group pull-right"
                ),
                Div(css_class="clearfix")
            )

        )
