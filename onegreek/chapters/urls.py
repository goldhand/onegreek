try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from .views import ChapterDetail, ChapterList


urlpatterns = patterns("events.views",
                       url(r"^$", ChapterList.as_view(), name='list'),
                       url(r"^(?P<pk>\d+)/$", ChapterDetail.as_view(), name='detail'),
                       )
