try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from .views import EventDetail, EventList, EventCreate, EventCreateJSON, EventDelete, EventUpdate


urlpatterns = patterns("events.views",
                       url(r"^$", EventList.as_view(template_name='events/event_list_calendar.html'), name='list'),
                       #url(r"^$", EventList.as_view(), name='list'),
                       url(r"^create/$", EventCreate.as_view(), name='create'),
                       url(r"^create/json/$", EventCreateJSON.as_view(), name='create_json'),
                       url(r"^(?P<pk>\d+)/$", EventDetail.as_view(), name='detail'),
                       url(r"^(?P<pk>\d+)/update$", EventUpdate.as_view(), name='update'),
                       url(r"^(?P<pk>\d+)/delete/$", EventDelete.as_view(), name='delete'),
                       url(r"^(?P<event_id>\d+)/rsvp/$", 'rsvp_event', name='rsvp'),
                       url(r"^(?P<event_id>\d+)/attend/$", 'attend_event', name='attend'),
                       #url(r"^calendar/(?P<year>\d+)/(?P<month>\d+)/$", 'calendar', name='calendar'),
                       #url(r"^calendar/$", CalendarRedirectView.as_view(), name='calendar-redirect'),
)

