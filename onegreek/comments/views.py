from rest_framework import viewsets

from .serializers import CommentSerializer
from .models import Comment

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
