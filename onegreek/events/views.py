from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, filters

from guardian.shortcuts import get_objects_for_user
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .serializers import EventSerializer, EventNestedSerializer
from .models import Event, EventCalendar, Attendees
from .permissions import EventObjectPermissions
from .forms import EventForm

User = get_user_model()

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (filters.DjangoObjectPermissionsFilter,)
    permission_classes = (EventObjectPermissions,)

    def pre_save(self, obj):
        obj.owner = self.request.user

    def get_serializer_class(self):
        if 'nest' in self.request.GET:
            if self.request.GET['nest']:
                return EventNestedSerializer

        return EventSerializer


class EventDetail(generic.DetailView):
    model = Event


class EventList(generic.ListView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super(EventList, self).get_context_data(**kwargs)
        context.update(event_form=EventForm())
        return context


@api_view(['GET', 'POST'])
@renderer_classes((JSONRenderer,))
def rsvp_event(request, event_id, format=None):
    event = get_object_or_404(Event, id=event_id)
    response = {'success': False, 'rsvp': False, 'display': 'not attending'}
    attendees = []

    if event:
        attendees = event.get_attendees_object()

    if request.method == "POST":
        if request.user in attendees.rsvps.all():
            attendees.rsvps.remove(request.user)
        else:
            attendees.rsvps.add(request.user)
            response['rsvp'] = True
            response['display'] = 'attending'
        attendees.save()
        response['success'] = True
    else:
        response['success'] = True
        if request.user in attendees.rsvps.all():
            response['rsvp'] = True
            response['display'] = 'attending'

    return Response(response)


@api_view(['GET', 'POST'])
@renderer_classes((JSONRenderer,))
def attend_event(request, event_id, format=None):
    event = get_object_or_404(Event, id=event_id)
    response = {'success': False, 'attend': False, 'display': 'did not attend'}
    attendees = []
    user = request.user

    if event:
        attendees = event.get_attendees_object()

    if 'attendee' in request.GET:
        user = get_object_or_404(User, id=request.GET['attendee'])

    if request.method == "POST":
        if user in attendees.attendees.all():
            attendees.attendees.remove(user)
        else:
            attendees.attendees.add(user)
            response['attend'] = True
            response['display'] = 'attended'
        attendees.save()
        response['success'] = True
    else:
        response['success'] = True
        if user in attendees.attendees.all():
            response['attend'] = True
            response['display'] = 'attended'

    return Response(response)


from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe


def calendar(request, year, month):
    my_events = get_objects_for_user(request.user, 'events.view_event').order_by('start').filter(
        start__year=year, start__month=month
    )
    cal = EventCalendar(my_events).formatmonth(int(year), int(month))
    return render(request, 'events/calendar.html', {'calendar': mark_safe(cal), })


class CalendarRedirectView(generic.RedirectView):
    permanent = False

    def get_redirect_url(self):
        redirect_url = reverse("events:calendar", kwargs={"year": 2013, "month": 11})
        return redirect_url
