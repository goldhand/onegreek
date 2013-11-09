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
            'title', 'description', 'university', 'fraternity',
            'cost', 'gpa',
            'description', 'awards', 'philanthropy', 'potential_new_members',
            'slug', 'group',
            ]
        widgets = {
            'group': forms.HiddenInput(),
            'slug': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        #kwargs.update(scope_prefix='event')
        super(ChapterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        #self.helper.form_tag = False
        #self.helper.form_action =
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('title', css_class="input-block-level"),
                    Field('fraternity', css_class="input-block-level"),
                    Field('university', css_class="input-block-level"),
                    Field('cost', css_class="input-block-level"),
                    Field('gpa', css_class="input-block-level"),
                    Field('description', css_class="input-block-level", rows='6'),
                    css_class="span6"
                ),
                Div(
                    Field('awards', css_class="input-block-level", rows='6'),
                    Field('philanthropy', css_class="input-block-level", rows='6'),
                    Field('potential_new_members', css_class="input-block-level", rows='6'),
                    'slug', 'group',
                    css_class="span6"
                ),
                css_class='row',
            ),
            Submit('submit', 'Submit')

        )
