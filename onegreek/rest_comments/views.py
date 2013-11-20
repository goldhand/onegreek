
from rest_framework import viewsets
from rest_framework.decorators import api_view

from .serializers import RestCommentSerializer
from .models import RestComment


class CommentViewSet(viewsets.ModelViewSet):
    queryset = RestComment.objects.all()
    serializer_class = RestCommentSerializer

    def create(self, request, *args, **kwargs):
        if not 'content_type_id' in request.POST:
            print 'no content type, using chapter group'
            request.POST['content_type_id'] = 2
            request.POST['object_pk'] = request.user.chapter.linked_group.id
            print request.POST
        return super(CommentViewSet, self).create(request, *args, **kwargs)


