try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from .views import EventDetail, EventList


urlpatterns = patterns("events.views",
                       url(r"^$", EventList.as_view(), name='list'),
                       url(r"^(?P<pk>\d+)/$", EventDetail.as_view(), name='detail'),
                       url(r"^(?P<event_id>\d+)/rsvp/$", 'rsvp_event', name='rsvp'),
                       url(r"^(?P<event_id>\d+)/attend/$", 'attend_event', name='attend'),
                       url(r"^calendar/(?P<year>\d+)/(?P<month>\d+)/$", 'calendar', name='calendar'),
)

