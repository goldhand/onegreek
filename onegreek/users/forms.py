# -*- coding: utf-8 -*-
from django import forms

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit, Button, Fieldset, HTML

from djangular.forms.angular_model import NgModelFormMixin

from phonenumber_field.formfields import PhoneNumberField

from django.core.exceptions import ValidationError

from .models import User


def validate_phone_number(value):
    if len(value) != 10:
        raise ValidationError(u'%s is not a ten digit phone number' % value)

def validate_gpa(value):
    if value < 0 or value > 4:
        raise ValidationError(u'%s is not a valid gpa between 0.0 and 4.0' % value)

def validate_hs_gpa(value):
    if value < 0 or value > 5:
        raise ValidationError(u'%s is not a valid gpa between 0.0 and 5.0' % value)



rush_or_active_toggle_widget = \
    '<div class="control-group">' \
    '<div class="controls">' \
    '<div class="btn-group" id="rush-or-active">' \
    '<button type="button" class="btn btn-primary" ng-click="userForm.reveal(\'rush\')"' \
    'ng-model="user.rush" btn-radio="true">Rushee</button>' \
    '<button type="button" class="btn btn-primary" ng-click="userForm.reveal(\'active\')"' \
    'ng-model="user.rush" btn-radio="false">Active</button>' \
    '</div>' \
    '</div>' \
    '</div>'


class UserRegisterForm(NgModelFormMixin, forms.ModelForm):
    phone = forms.CharField(validators=[validate_phone_number], label='Phone Number, digits only (e.g 1114443333)', required=True)
    highschool_gpa = forms.FloatField(validators=[validate_hs_gpa], required=False)
    gpa = forms.FloatField(validators=[validate_gpa], label='Current College GPA (if applicable)', required=False)

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        # Set this form to use the User model.
        model = User

        # Constrain the UserForm to just these fields.
        fields = (
            "first_name",
            "last_name",
            "phone",
            "chapter",
            'gpa',
            "highschool_gpa",
            "year",
            "major",
            #"gpa",
            "hometown",
            #"status"
        )

    def __init__(self, *args, **kwargs):
        kwargs.update(scope_prefix='globals.user')
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('first_name', css_class=""),
                    Field('last_name', css_class=""),
                    Field('year', css_class=""),
                    Field('phone', css_class=""),
                    HTML(rush_or_active_toggle_widget),
                    css_class="span6"
                ),
                HTML('<div ng-show="userForm.part2">'),
                HTML('<div ng-show="user.rush">'),
                Div(
                    Field('major', css_class=""),
                    Field('gpa', css_class=""),
                    Field('highschool_gpa', css_class=""),
                    Field('hometown', css_class=""),
                    #Field('phone', css_class=""),
                    #Field('chapter', css_class=""),
                    #Field('gpa', css_class=""),
                    HTML(
                        '<div ng-show="globals.user.hometown.length">'
                        + '<div class="form-actions" ng-show="globals.user.major.length">'
                        + '<input class="btn btn-primary pull-right" type="submit" value="Continue">'
                        + '</div></div>'
                    ),
                    css_class="span6"
                ),
                HTML('</div>'),
                HTML('<div ng-hide="user.rush">'),
                Div(
                    Field('chapter', css_class=""),
                    HTML(
                        '<div class="form-actions" '
                        + 'ng-show="globals.user.chapter.length">'
                        + '<input class="btn btn-primary pull-right" type="submit" value="Continue">'
                        + '</div>'
                    ),
                    css_class="span6"
                ),
                HTML('</div>'),
                HTML('</div>'),
                css_class=""

            )
        )


class UserForm(forms.ModelForm):
    phone = forms.CharField(validators=[validate_phone_number], required=True)

    class Meta:
        # Set this form to use the User model.
        model = User

        # Constrain the UserForm to just these fields.
        fields = (
            "first_name",
            "last_name",
            "phone",
            #"chapter",
            "gpa",
            "highschool_gpa",
            "year",
            "major",
            "hometown",
            #"status"
        )

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Field('first_name', css_class=""),
            Field('last_name', css_class=""),
            Fieldset(
                'Profile Details',
                Field('phone', css_class=""),
                Field('year', css_class=""),
                Field('major', css_class=""),
                Field('gpa', css_class=""),
                Field('highschool_gpa', css_class=""),
                Field('hometown', css_class=""),
                #Field('phone', css_class=""),
                #Field('chapter', css_class=""),
            ),
        )


from avatar.forms import UploadAvatarForm, DeleteAvatarForm, PrimaryAvatarForm


class UploadAvatarFormNu(UploadAvatarForm):

    def __init__(self, *args, **kwargs):
        super(UploadAvatarFormNu, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        #self.helper.form_tag = False
        #self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                'Upload Avatar',
                Field('avatar', css_class=""),
            )
        )


class DeleteAvatarFormNu(DeleteAvatarForm):
    pass



class PrimaryAvatarFormNu(PrimaryAvatarForm):
    pass
