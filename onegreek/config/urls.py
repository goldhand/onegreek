# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
                       #url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name="home"),
                       url(r'^$', 'config.views.home_view', name="home"),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^users/', include("users.urls", namespace="users")),
                       url(r'^accounts/', include('allauth.urls')),
                       url(r'^avatar/', include('avatar.urls')),
                       url(r'^comments/', include('django_comments.urls')),
                       url(r'^gallery/', include('imagestore.urls', namespace='imagestore')),
                       url(r'^api/', include('apiroot.urls')),
                       url(r'^events/', include('events.urls', namespace='events')),
                       url(r'^chapters/', include('chapters.urls', namespace='chapters')),
                       url(r'^rush/forms/', include('rush_forms.urls', namespace='rush-forms')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
