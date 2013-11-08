from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(view_name='user-detail', blank=True)
    title = serializers.WritableField(source='title', blank=True)
    description = serializers.WritableField(source='description', blank=True)
    chapter = serializers.HyperlinkedRelatedField('get_chapter', view_name='chapter-detail', read_only=True)
    viewers = serializers.HyperlinkedRelatedField(many=True, view_name='chapter-detail', blank=True)
    attendees = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', blank=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'url', 'title', 'description',
            'start', 'end', 'owner', 'enable_comments',
            'viewers', 'attendees',
            #'chapter',
        ]
