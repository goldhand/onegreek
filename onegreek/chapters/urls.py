try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from .views import ChapterDetail, ChapterList, ChapterUpdate
from .forms import ChapterForm
from .preview import ChapterFormPreview


urlpatterns = patterns("chapters.views",
                       url(r"^$", ChapterList.as_view(), name='list'),
                       url(r"^(?P<pk>\d+)/$", ChapterDetail.as_view(), name='detail'),
                       url(r"^update/(?P<pk>\d+)/$", ChapterUpdate.as_view(), name='update'),
                       url(r"^post/$", ChapterFormPreview(ChapterForm), name='post'),
                       url(r"^rush/(?P<pk>\d+)/$", 'rush_chapter_view', name='rush'),
                       )
