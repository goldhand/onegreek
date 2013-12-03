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
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .forms import UserForm

# Import the customized User model
User = get_user_model() # use this function for swapping user model
from django.contrib.auth.models import Group


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "pk"
    slug_url_kwarg = "pk"


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
