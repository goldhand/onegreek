# -*- coding: utf-8 -*-
from django import forms

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit, Button, Fieldset, HTML

from djangular.forms.angular_model import NgModelFormMixin

from .models import User


class UserForm(NgModelFormMixin, forms.ModelForm):

    class Meta:
        # Set this form to use the User model.
        model = User

        # Constrain the UserForm to just these fields.
        fields = (
            "first_name",
            "last_name",
            "phone",
            "chapter",
            "highschool_gpa",
            "year",
            "major",
            "gpa",
            "hometown",
            #"status"
        )

    def __init__(self, *args, **kwargs):
        kwargs.update(scope_prefix='event')
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('first_name', css_class=""),
                    Field('last_name', css_class=""),
                    Field('chapter', css_class=""),
                    css_class="span6"
                ),
                Div(
                    Field('phone', css_class=""),
                    Field('highschool_gpa', css_class=""),
                    Field('year', css_class=""),
                    Field('major', css_class=""),
                    Field('gpa', css_class=""),
                    Field('hometown', css_class=""),
                    css_class="span6"
                ),
                css_class="row"

            )
        )


