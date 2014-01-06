import datetime
from crispy_forms.utils import render_crispy_form

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.forms.formsets import formset_factory

from guardian.shortcuts import get_objects_for_user

from rest_framework import viewsets, filters
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from jsonview.decorators import json_view

from imagestore.forms import ImageForm, ImageFormCrispy

from .serializers import EventSerializer, EventNestedSerializer
from .models import Event, EventCalendar, Attendees
from .permissions import EventObjectPermissions
from .forms import EventForm, EventFormFlat

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

    def get_queryset(self):
        queryset = super(EventViewSet, self).get_queryset()
        if 'rush_week' in self.request.GET:
            if self.request.GET['rush_week']:
                now = datetime.datetime.now()
                start_date = now.replace(day=1, hour=1)
                end_date = now.replace(day=1, hour=1)
                if now.month <= 4:
                    start_date = start_date.replace(month=1)
                    end_date = end_date.replace(month=6)
                elif now.month >= 11:
                    start_date = start_date.replace(year=now.year + 1, month=1)
                    end_date = end_date.replace(year=now.year + 1, month=6)
                else:
                    start_date = start_date.replace(month=7)
                    end_date = end_date.replace(month=12)

                queryset = queryset.filter(status='rush').filter(start__range=(start_date, end_date))

        return queryset


class EventDetail(generic.DetailView):
    model = Event


class EventCreate(generic.CreateView):
    model = Event
    form_class = EventFormFlat

    def get_context_data(self, **kwargs):
        context = super(EventCreate, self).get_context_data(**kwargs)
        context['image_form'] = ImageFormCrispy(user=self.request.user, **self.get_form_kwargs())
        context.update(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        return super(EventCreate, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(EventCreate, self).form_valid(form)


class EventCreateJSON(generic.CreateView):
    model = Event
    form_class = EventFormFlat

    @json_view
    def dispatch(self, *args, **kwargs):
        return super(EventCreateJSON, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        if 'id_status' in self.request.POST:
            form.instance.status = self.request.POST['id_status']
        form.save()
        image_form_html = render_crispy_form(
            ImageFormCrispy(
                user=self.request.user,
                content_type=form.instance.get_content_type_id(),
                object_pk=form.instance.id
            ))
        context = {'success': True,
                   'image_form_html': image_form_html,
                   'id': form.instance.id,
                   'ctype_id': form.instance.get_content_type_id()}
        #return super(EventCreateJSON, self).form_valid(form)
        return context

    def form_invalid(self, form):
        image_form_html = render_crispy_form(form)
        return {'success': False, 'form_html': image_form_html}

    def get(self, request, *args, **kwargs):
        form_html = render_crispy_form(self.form_class)
        context = {'form_html': form_html}
        return context


class EventDelete(generic.DeleteView):
    model = Event
    success_url = reverse_lazy("events:list")

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

    if 'user_id' in request.GET:
        user = get_object_or_404(User, pk=request.GET['user_id'])
    else:
        user = request.user

    if request.method == "POST":

        if user in attendees.rsvps.all():
            attendees.rsvps.remove(user)
        else:
            attendees.rsvps.add(user)
            response['rsvp'] = True
            response['display'] = 'attending'
        attendees.save()
        response['success'] = True
    else:
        response['success'] = True
        if user in attendees.rsvps.all():
            response['rsvp'] = True
            response['display'] = 'attending'

    return Response(response)


@api_view(['GET', 'POST'])
@renderer_classes((JSONRenderer,))
def attend_event(request, event_id, format=None):
    event = get_object_or_404(Event, id=event_id)
    response = {'success': False, 'attend': False, 'display': 'did not attend'}
    attendees = []
    if 'user_id' in request.GET:
        user = get_object_or_404(User, pk=request.GET['user_id'])
    else:
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


@api_view(['GET', 'POST'])
@renderer_classes((JSONRenderer,))
def calendar(request, year, month):
    my_events = get_objects_for_user(request.user, 'events.view_event').order_by('start').filter(
        start__year=year, start__month=month
    )
    cal_template = 'events/calendar.html'

    if 'rsvp' in request.GET:
        if request.GET['rsvp']:
            #self.events = self.group_by_day([event for event in events.event])
            my_events = [attending.event for attending in request.user.get_rsvps()]
    elif 'profile' in request.GET:
        if request.GET['profile']:
            cal_template = 'events/calendar-profile.html'

    cal = EventCalendar(my_events).formatmonth(int(year), int(month))

    return Response({'calendar': mark_safe(cal)})


class CalendarRedirectView(generic.RedirectView):
    permanent = False

    def get_redirect_url(self):
        redirect_url = reverse("events:calendar", kwargs={"year": 2013, "month": 11})
        return redirect_url
