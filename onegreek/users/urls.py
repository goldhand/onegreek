# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from users import views

urlpatterns = patterns('',
    # URL pattern for the UserListView
    url(
        regex=r'^alt/$',
        view=views.UserListView.as_view(),
        name='list-alt'
    ),
    url(
        regex=r'^~$',
        view=views.UserListView.as_view(template_name='users/user_list_alt.html'),
        name='list'
    ),
    # URL pattern for the UserRedirectView
    url(
        regex=r'^$',
        view=views.UserRedirectView.as_view(),
        name='redirect'
    ),
    # URL pattern for the UserDetailView
    url(
        regex=r'^(?P<pk>\d+)/$',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),
    url(
        regex=r'^group/mod/$',
        view='users.views.mod_group',
        name='mod-group'
    ),
    url(
        regex=r'^mod/$',
        view='users.views.mod_user_groups',
        name='mod-user-groups'
    ),
    url(
        regex=r'^group/call/$',
        view='users.views.call_list',
        name='call-list'
    ),
    # URL pattern for the UserUpdateView
    url(
        regex=r'^~update/$',
        view=views.UserUpdateView.as_view(),
        name='update'
    ),
)