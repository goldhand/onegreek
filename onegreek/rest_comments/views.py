
from rest_framework import viewsets
from rest_framework.decorators import api_view

import comments
from comments import signals
from comments.utils import next_redirect, confirmation_view

from comments.serializers import CommentSerializer
from comments.models import Comment


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        if not 'content_type_id' in request.POST:
            print 'no content type, using chapter group'
            request.POST['content_type_id'] = 2
            request.POST['object_pk'] = request.user.chapter.linked_group.id
            print request.POST
        return super(CommentViewSet, self).create(request, *args, **kwargs)


