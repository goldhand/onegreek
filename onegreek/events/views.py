from django.views import generic

from rest_framework import viewsets
from rest_framework import permissions

from .serializers import EventSerializer
from .models import Event
from .permissions import IsOwnerOrViewer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrViewer
    )

class EventDetail(generic.DetailView):
    model = Event