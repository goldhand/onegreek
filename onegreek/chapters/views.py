import logging
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.views import generic
from django.views.generic import edit
from django.contrib import messages

from rest_framework import viewsets
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, YAMLRenderer

from .models import Chapter
from rush_forms.forms import FormForForm
from rush_forms.models import Form as RushForm
from .serializers import ChapterSerializer
from .forms import ChapterForm

logger = logging.getLogger(__name__)


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer


class ChapterDetail(generic.DetailView):
    model = Chapter

    def get_context_data(self, **kwargs):
        context = super(ChapterDetail, self).get_context_data(**kwargs)
        _object = super(ChapterDetail, self).get_object()
        form = FormForForm(_object.get_rush_form(), self.request.POST or None, self.request.FILES or None)
        context['rush_form'] = form
        context.update(**kwargs)
        return context


class ChapterCreate(generic.CreateView):
    model = Chapter
    form_class = ChapterForm


class ChapterUpdate(generic.UpdateView):
    model = Chapter
    form_class = ChapterForm


class ChapterList(generic.ListView):
    model = Chapter

    def get_context_data(self, **kwargs):
        context = super(ChapterList, self).get_context_data(**kwargs)
        context.update(form=ChapterForm())
        return context

    def post(self, request, *args, **kwargs):
        view = ChapterCreate.as_view()
        return view(request, *args, **kwargs)


@api_view(['GET', 'POST'])
@renderer_classes((JSONRenderer,))
def rush_chapter_view(request, pk, format=None):
    chapter = get_object_or_404(Chapter, pk=pk)
    hide = True
    success = False
    title = 'Sign up to rush %s' % chapter.fraternity_title
    disabled = True
    message = ''
    rushing = False
    if request.user.is_authenticated() and not request.user.chapter:
        rush_group = chapter.linked_rush_group
        hide = False
        disabled = False
        title = 'Rush %s' % chapter.fraternity_title
        if rush_group:
            if request.user in rush_group.user_set.all():

                if request.method == "POST":
                    rush_group.user_set.remove(request.user.id)
                    message = 'You no longer Rushing %s, %s chapter' % (chapter.fraternity_title, chapter.title)
                else:
                    title = 'Stop Rushing %s' % chapter.fraternity_title
                    rushing = True
            else:
                if request.method == "POST":
                    rush_group.user_set.add(request.user.id)
                    message = 'You are now Rushing %s, %s chapter' % (chapter.fraternity_title, chapter.title)
                    title = 'Stop Rushing %s' % chapter.fraternity_title
                    rushing = True
                    #messages.success(request, message)
            success = True
    else:
        if not request.user.is_authenticated():
            hide = False
            message = ''
        success = True

    return Response({
        'success': success,
        'title': title,
        'message': message,
        'hide': hide,
        'disabled': disabled,
        'rushing': rushing
    })

