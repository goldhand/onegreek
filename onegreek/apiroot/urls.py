try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from rest_framework.routers import DefaultRouter

from chapters.views import ChapterViewSet
from users.views import UserViewSet
from comments.views import CommentViewSet
from events.views import EventViewSet
from universities.views import UniversityViewSet

router = DefaultRouter()
router.register(r'chapters', ChapterViewSet)
router.register(r'users', UserViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'events', EventViewSet)
router.register(r'universities', UniversityViewSet)

urlpatterns = patterns('chapters.views',
                       url(r'^', include(router.urls)),
                       )