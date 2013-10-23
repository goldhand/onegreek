from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(view_name='user-detail')
    description = serializers.WritableField(source='description')
    chapter = serializers.HyperlinkedRelatedField('get_chapter', view_name='chapter-detail', read_only=True)
    viewers = serializers.HyperlinkedRelatedField(many=True, view_name='chapter-detail')
    attendees = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail')

    class Meta:
        model = Event
        fields = [
            'url', 'title', 'description',
            'start', 'end', 'owner', 'chapter',
            'viewers', 'attendees'
        ]
