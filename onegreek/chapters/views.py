from django.views import generic
from rest_framework import viewsets

from .models import Chapter
from .serializers import ChapterSerializer
from .forms import ChapterForm

class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer


class ChapterDetail(generic.DetailView):
    model = Chapter


class ChapterList(generic.ListView):
    model = Chapter

    def get_context_data(self, **kwargs):
        context = super(ChapterList, self).get_context_data(**kwargs)
        context.update(chapter_form=ChapterForm())
        return context
