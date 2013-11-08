from django import forms

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit, Button, Fieldset, HTML

from djangular.forms.angular_model import NgModelFormMixin

from .models import Chapter



class ChapterForm(NgModelFormMixin, forms.ModelForm):
    class Meta:
        model = Chapter
        fields = [
            'title', 'description', 'university',
            'cost', 'gpa',
            'description', 'awards', 'philanthropy', 'potential_new_members',
            'slug', 'group',
            ]
        widgets = {
            'group': forms.HiddenInput(),
            'slug': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        kwargs.update(scope_prefix='event')
        super(ChapterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Div(
                'title',
                'description',
                'university',
                'cost', 'gpa',
                'description',
                'awards',
                'philanthropy',
                'potential_new_members',
                'slug', 'group',
            )
        )
