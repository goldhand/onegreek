from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(view_name='user-detail')
    viewers = serializers.HyperlinkedRelatedField(many=True, view_name='chapter-detail')
    content = serializers.WritableField(source='content')

    class Meta:
        model = Comment
        fields = [
            'url', 'owner', 'content',
            'status', 'created', 'modified',
            'viewers'
        ]
