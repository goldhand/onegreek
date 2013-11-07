try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from .views import EventDetail, EventList


urlpatterns = patterns("events.views",
                       url(r"^$", EventList.as_view(), name='list'),
                       url(r"^(?P<pk>\d+)/$", EventDetail.as_view(), name='detail'),
)

