from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, filters

from .serializers import EventSerializer
from .models import Event
from .permissions import EventObjectPermissions
from .forms import EventForm

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (filters.DjangoObjectPermissionsFilter,)
    permission_classes = (EventObjectPermissions,)

    def pre_save(self, obj):
        obj.owner = self.request.user


class EventDetail(generic.DetailView):
    model = Event


class EventList(generic.ListView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super(EventList, self).get_context_data(**kwargs)
        context.update(event_form=EventForm())
        return context