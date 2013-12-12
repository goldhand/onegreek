# -*- coding: utf-8 -*-
from django import forms

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit, Button, Fieldset, HTML

from djangular.forms.angular_model import NgModelFormMixin

from .models import User

rush_or_active_toggle_widget = \
    '<div class="control-group">' \
    '<label for="rush-or-active" class="control-label">Are you </label>' \
    '<div class="controls">' \
    '<div class="btn-group" id="rush-or-active">' \
    '<button type="button" class="btn btn-primary" ng-click="userForm.reveal(\'rush\')"' \
    'ng-model="user.rush" btn-radio="true">Rush</button>' \
    '<button type="button" class="btn btn-primary" ng-click="userForm.reveal(\'active\')"' \
    'ng-model="user.rush" btn-radio="false">Active</button>' \
    '</div>' \
    '</div>' \
    '</div>'


class UserForm(NgModelFormMixin, forms.ModelForm):

    class Meta:
        # Set this form to use the User model.
        model = User

        # Constrain the UserForm to just these fields.
        fields = (
            "first_name",
            "last_name",
            #"phone",
            "chapter",
            "highschool_gpa",
            "year",
            "major",
            #"gpa",
            "hometown",
            #"status"
        )

    def __init__(self, *args, **kwargs):
        kwargs.update(scope_prefix='globals.user')
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('first_name', css_class=""),
                    Field('last_name', css_class=""),
                    Field('year', css_class=""),
                    HTML(rush_or_active_toggle_widget),
                    css_class="span6"
                ),
                HTML('<div ng-show="userForm.part2">'),
                HTML('<div ng-show="user.rush">'),
                Div(
                    Field('major', css_class=""),
                    Field('highschool_gpa', css_class=""),
                    Field('hometown', css_class=""),
                    #Field('phone', css_class=""),
                    #Field('chapter', css_class=""),
                    #Field('gpa', css_class=""),
                    HTML(
                        '<div ng-show="globals.user.major.length">'
                        + '<div ng-show="globals.user.highschool_gpa != null">'
                        + '<div class="form-actions">'
                        + '<input class="btn btn-primary pull-right" type="submit" value="Continue" '
                        + 'ng-show="globals.user.hometown.length">'
                        + '</div></div></div>'
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


class UserEditForm(forms.ModelForm):

    class Meta:
        # Set this form to use the User model.
        model = User

        # Constrain the UserForm to just these fields.
        fields = (
            "first_name",
            "last_name",
            #"phone",
            #"chapter",
            "gpa",
            "highschool_gpa",
            "year",
            "major",
            "hometown",
            #"status"
        )

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Field('first_name', css_class=""),
            Field('last_name', css_class=""),
            Fieldset(
                'Profile Details',
                Field('year', css_class=""),
                Field('major', css_class=""),
                Field('gpa', css_class=""),
                Field('highschool_gpa', css_class=""),
                Field('hometown', css_class=""),
                #Field('phone', css_class=""),
                #Field('chapter', css_class=""),
            )
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
