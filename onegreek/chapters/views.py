from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.generic import edit

from rest_framework import viewsets

from .models import Chapter
from .serializers import ChapterSerializer
from .forms import ChapterForm


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer



class ChapterDetail(generic.DetailView):
    model = Chapter


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

from django.shortcuts import redirect


def rush_chapter_view(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    rush_group = chapter.linked_rush_group
    if rush_group:
        rush_group.user_set.add(request.user.id)
        print rush_group.user_set.all()
    return redirect(chapter)

