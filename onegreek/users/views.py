# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

# view imports
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.contrib.auth import get_user_model

# Only authenticated users can access views using this.
from braces.views import LoginRequiredMixin

# Import the form from users/forms.py
from django.views.generic.edit import FormMixin
from django.contrib import messages
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from avatar.forms import UploadAvatarForm, DeleteAvatarForm, PrimaryAvatarForm

from .forms import UserForm, UserRegisterForm, UploadAvatarFormNu, DeleteAvatarFormNu, PrimaryAvatarFormNu

# Import the customized User model
User = get_user_model() # use this function for swapping user model
from django.contrib.auth.models import Group


class UserDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = User
    form_class = UserForm
    # These next two lines tell the view to index lookups by username
    slug_field = "pk"
    slug_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        avatars = self.get_object().avatar_set.all()
        context['avatars'] = avatars
        context['profile_form'] = self.form_class(instance=self.get_object())
        context['avatar_upload_form'] = UploadAvatarFormNu(user=self.get_object())
        context['avatar_primary_form'] = PrimaryAvatarForm(user=self.get_object(), avatars=avatars)
        context['avatar_delete_form'] = DeleteAvatarForm(user=self.get_object(), avatars=avatars)
        return context

    def get_success_url(self):
        messages.success(self.request, 'Successfully updated your profile', 'success')
        if 'next' in self.request.GET:
            return self.request.GET['next']
        else:
            return reverse("users:edit")


class UserRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self):
        user = self.request.user
        redirect_url = reverse('account_login')
        # is user anon?
        if user.is_authenticated():
            # is user an active of a chapter?
            if user.chapter_id:
                # yes
                redirect_url = reverse("chapters:detail", kwargs={"pk": user.chapter_id})
            else:
                # no
                redirect_url = reverse("chapters:list")

        return redirect_url


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserForm

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        messages.success(self.request, 'Successfully updated your profile', 'success')
        if 'next' in self.request.GET:
            return self.request.GET['next']
        else:
            return reverse("users:redirect")

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(pk=self.request.user.pk)





class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "pk"
    slug_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context.update(user_form=UserForm())
        return context


from rest_framework import viewsets

from .serializers import UserSerializer, GroupSerializer, GroupUpdateSerializer, GroupCreateSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        q = super(UserViewSet, self).get_queryset()
        if 'group' in self.request.GET:
            return q.filter(groups__id=self.request.GET['group'])
        elif 'chapter' in self.request.GET:
            chapter_id = self.request.GET['chapter']
            if 'rush' in self.request.GET:
                return q.filter(groups__name__istartswith='chapter_%s' % chapter_id).distinct()
            else:
                return q.filter(chapter_id=chapter_id).exclude(status="active_pending")
        else:
            chapter_id = self.request.user.chapter_id
            if chapter_id:
                return q.filter(groups__name__istartswith='chapter_%d' % chapter_id).distinct()
            else:
                return q


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request, *args, **kwargs):
        self.serializer_class = GroupCreateSerializer
        return super(GroupViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = GroupUpdateSerializer
        return super(GroupViewSet, self).update(request, *args, **kwargs)

    def get_queryset(self):
        q = super(GroupViewSet, self).get_queryset()
        return q.filter(chapter__id=self.request.user.chapter_id)


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
def mod_group(request, format=None):
    if 'group_id' in request.DATA and 'action' in request.DATA \
        and 'chapter_id' in request.DATA and 'user_set' in request.DATA:
        group = get_object_or_404(Group, id=request.DATA['group_id'])
        action = request.DATA['action']
        chapter_id = request.DATA['chapter_id']
        user_set = request.DATA['user_set']
        for user_id in user_set:
            user = get_object_or_404(User, id=user_id)
            user.groups.clear()
            user.status = 'rush'
            user.chapter = None
            user.save()
        response = {'success': True}
    else:
        response = {'success': False}
    return Response(response)


@api_view(['GET', 'POST'])
@renderer_classes((JSONRenderer,))
def call_list(request, format=None):
    user_id = request.DATA['user_id']
    group_id = request.DATA['group_id']
    action = request.DATA['action']
    user = get_object_or_404(User, id=user_id)
    if action == "add":
        user.groups.add(group_id)
    elif action == "remove":
        user.groups.remove(group_id)
    user.save()
    response = {'success': True}
    return Response(response)


from chapters.models import Chapter

@api_view(['GET', 'POST'])
@renderer_classes((JSONRenderer,))
def mod_user_groups(request, format=None):

    user_id = request.DATA['user_id']
    chapter_id = request.DATA['chapter_id']
    status = request.DATA['status']
    new_status = request.DATA['new_status']
    action = request.DATA['action']

    user = get_object_or_404(User, id=user_id)
    chapter = get_object_or_404(Chapter, id=chapter_id)
    group = None
    new_group = None

    response = {
        'success': False,
        'user_full_name': user.get_full_name(),
        'action': action,
        'status': status,
        'new_status': new_status
    }


    if status == 'active':
        group = chapter.linked_active_group
    elif status == 'active_pending':
        group = chapter.linked_pending_group
    elif status == 'rush':
        group = chapter.linked_rush_group
    elif status == 'pledge':
        group = chapter.linked_pledge_group
    elif status == 'admin':
        group = chapter.linked_admin_group


    if new_status == 'active':
        new_group = chapter.linked_active_group
    elif new_status == 'active_pending':
        new_group = chapter.linked_pending_group
    elif new_status == 'rush':
        new_group = chapter.linked_rush_group
    elif new_status == 'pledge':
        new_group = chapter.linked_pledge_group
    elif new_status == 'admin':
        new_group = chapter.linked_admin_group
    elif new_status == 'call':
        new_group = chapter.linked_call_group


    if group:
        if action == "add":

            user.groups.add(new_group.id)

            # admin is not a status
            if status != 'admin':

                # rush uses a different 'add' action than other status
                if status == 'rush':
                    if new_status != 'call':
                        # If action: add and status: rush and not new status: call the user is being added to chapter
                        user.groups.remove(group.id)
                        # remove from rush group here because 'add' action won't remove groups otherwise
                        user.chapter = chapter
                        # set chapter for new member
                        user.status = new_status
                    else:
                        user.groups.add(new_group.id)
                else:
                    user.status = status

                response['status'] = user.status

        elif action == "remove":

            if new_status != 'call':
                # not removing from call list
                user.groups.remove(group.id)
                user.groups.add(new_group.id)

                if new_status == 'rush':
                    user.chapter = None

                    # If action: remove and status: active_pending the user is being removed permanently
                    if status == 'active_pending':
                        user.groups.remove(new_group.id)

                user.status = new_status
            else:
                # remove from call list
                user.groups.remove(new_group.id)
        user.save()
        response['success'] = True

    return Response(response)


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def user_in_chapter_group(request, format=None):
    user_id = request.GET['check_user_id']
    chapter_id = request.GET['chapter_id']
    status = request.GET['status']
    # Not user.status as includes call and admin
    user = get_object_or_404(User, id=user_id)
    chapter = get_object_or_404(Chapter, id=chapter_id)
    group = None

    if status == 'active':
        group = chapter.linked_active_group
    elif status == 'active_pending':
        group = chapter.linked_pending_group
    elif status == 'rush':
        group = chapter.linked_rush_group
    elif status == 'pledge':
        group = chapter.linked_pledge_group
    elif status == 'admin':
        group = chapter.linked_admin_group
    elif status == 'call':
        group = chapter.linked_call_group

    _response = {
        'success': False,
        'status': status,
        'chapter': chapter.title,
        'user': user.get_full_name(),
        'in_group': False
    }
    if group:
        _response['success'] = True
        if group in user.groups.all():
            _response['in_group'] = True

    return Response(_response)
