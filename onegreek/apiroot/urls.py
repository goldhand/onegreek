try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from rest_framework.routers import DefaultRouter

from chapters.views import ChapterViewSet
from users.views import UserViewSet

router = DefaultRouter()
router.register(r'chapters', ChapterViewSet)
router.register(r'users', UserViewSet)

urlpatterns = patterns('chapters.views',
                       url(r'^', include(router.urls)),
                       )
