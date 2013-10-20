try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from rest_framework.routers import DefaultRouter

from .views import ChaperViewSet

router = DefaultRouter()
router.register(r'chapters', ChaperViewSet)

urlpatterns = patterns('chapters.views',
                       url(r'^', include(router.urls)),
)
