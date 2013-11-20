try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from rest_framework.routers import DefaultRouter

from chapters.views import ChapterViewSet
from fraternities.views import FraternityViewSet
from users.views import UserViewSet, GroupViewSet
from rest_comments.views import CommentViewSet
from events.views import EventViewSet
from universities.views import UniversityViewSet

router = DefaultRouter()
router.register(r'chapters', ChapterViewSet)
router.register(r'fraternities', FraternityViewSet)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'events', EventViewSet)
router.register(r'universities', UniversityViewSet)

urlpatterns = patterns('apiroot.views',
                       url(r'^', include(router.urls)),
                       )
