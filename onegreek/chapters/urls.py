try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from .views import ChapterDetail, ChapterList
from .forms import ChapterForm
from .preview import ChapterFormPreview


urlpatterns = patterns("events.views",
                       url(r"^$", ChapterList.as_view(), name='list'),
                       url(r"^(?P<pk>\d+)/$", ChapterDetail.as_view(), name='detail'),
                       url(r"^post/$", ChapterFormPreview(ChapterForm), name='post'),
                       )
