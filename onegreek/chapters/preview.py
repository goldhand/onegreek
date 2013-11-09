from django.contrib.formtools.preview import FormPreview
from django.http import HttpResponseRedirect

from .models import Chapter
from .serializers import ChapterSerializer
from .forms import ChapterForm


class ChapterFormPreview(FormPreview):

    def process_preview(self, request, cleaned_data):
        print "processed"

    def done(self, request, cleaned_data):
        f = self.form(request.POST)
        f.save()
        print 'Form saved'

        return HttpResponseRedirect('/chapters/')
